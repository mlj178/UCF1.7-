using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

public class DllInjector
{
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern IntPtr GetModuleHandle(string lpModuleName);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Ansi)]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string lpProcName);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, uint nSize, out int lpNumberOfBytesWritten);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool GetExitCodeThread(IntPtr hThread, out uint lpExitCode);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool IsWow64Process(IntPtr hProcess, out bool wow64Process);

    [DllImport("psapi.dll", SetLastError = true)]
    public static extern bool EnumProcessModulesEx(IntPtr hProcess, IntPtr[] lphModule, int cb, out int lpcbNeeded, int dwFilterFlag);

    [DllImport("psapi.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern int GetModuleFileNameEx(IntPtr hProcess, IntPtr hModule, StringBuilder lpFilename, int nSize);

    private const int PROCESS_ALL_ACCESS = 0x1F0FFF;
    private const uint MEM_COMMIT = 0x1000;
    private const uint MEM_RESERVE = 0x2000;
    private const uint PAGE_READWRITE = 0x04;
    private const int LIST_MODULES_32BIT = 0x01;

    private static string logFile = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "inject_log.txt");

    public static void Log(string message, string level)
    {
        // DISABLED: 日志输出已注释
        /*
        string timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");
        string line = string.Format("[{0}] [{1}] {2}", timestamp, level, message);
        Console.WriteLine(line);
        try { File.AppendAllText(logFile, line + "\n"); } catch { }
        */
    }

    public static IntPtr GetRemoteModuleBase(IntPtr hProcess, string moduleName)
    {
        IntPtr[] hModules = new IntPtr[1024];
        int cbNeeded = 0;

        if (!EnumProcessModulesEx(hProcess, hModules, hModules.Length * IntPtr.Size, out cbNeeded, LIST_MODULES_32BIT))
        {
            int error = Marshal.GetLastWin32Error();
            Log(string.Format("EnumProcessModulesEx失败，错误码: {0}", error), "ERROR");
            return IntPtr.Zero;
        }

        int moduleCount = cbNeeded / IntPtr.Size;
        Log(string.Format("枚举到 {0} 个模块", moduleCount), "INFO");

        for (int i = 0; i < moduleCount; i++)
        {
            StringBuilder sb = new StringBuilder(260);
            int len = GetModuleFileNameEx(hProcess, hModules[i], sb, sb.Capacity);
            if (len > 0)
            {
                string name = sb.ToString();
                Log(string.Format("模块[{0}]: {1}", i, name), "INFO");
                if (name.EndsWith(moduleName, StringComparison.OrdinalIgnoreCase))
                {
                    Log(string.Format("找到 {0}: 0x{1:X}", moduleName, hModules[i].ToInt64()), "INFO");
                    return hModules[i];
                }
            }
        }

        return IntPtr.Zero;
    }

    public static void Main(string[] args)
    {
        string processArg = args.Length > 0 ? args[0] : "UnityCrossFire";
        string dllPath = args.Length > 1 ? args[1] : Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Universal-ImGui-Hook.dll");

        // DISABLED: 日志分隔线已注释
        // try { File.AppendAllText(logFile, "\n" + new string('=', 60) + "\n"); } catch { }

        Log("DLL注入程序启动", "INFO");
        Log(string.Format("目标参数: {0}", processArg), "INFO");
        Log(string.Format("DLL路径: {0}", dllPath), "INFO");

        if (!File.Exists(dllPath))
        {
            Log(string.Format("错误: DLL文件不存在: {0}", dllPath), "ERROR");
            Environment.Exit(1);
            return;
        }
        Log(string.Format("DLL文件大小: {0} 字节", new FileInfo(dllPath).Length), "INFO");

        Process process = null;
        int pid;

        // Check if processArg is a PID (numeric)
        if (int.TryParse(processArg, out pid))
        {
            Log(string.Format("按 PID 查找进程: {0}", pid), "INFO");
            try
            {
                process = Process.GetProcessById(pid);
                Log(string.Format("找到进程: PID={0}, 主窗口: '{1}', 创建时间: {2}", 
                    process.Id, process.MainWindowTitle, process.StartTime), "INFO");
            }
            catch (ArgumentException)
            {
                Log(string.Format("错误: 进程 PID={0} 不存在", pid), "ERROR");
                Environment.Exit(1);
                return;
            }
        }
        else
        {
            // Find by process name
            string processName = processArg;
            Log(string.Format("按进程名查找: {0}", processName), "INFO");
            Process[] processes = Process.GetProcessesByName(processName);
            Log(string.Format("候选进程数量: {0}", processes.Length), "INFO");

            if (processes.Length > 0)
            {
                foreach (var p in processes)
                {
                    Log(string.Format("候选 PID={0}, Title='{1}', 创建时间: {2}", 
                        p.Id, p.MainWindowTitle, p.StartTime), "INFO");
                }
            }

            if (processes.Length == 0)
            {
                Log(string.Format("等待进程启动: {0}", processName), "INFO");
                for (int i = 0; i < 60; i++)
                {
                    System.Threading.Thread.Sleep(500);
                    processes = Process.GetProcessesByName(processName);
                    if (processes.Length > 0) break;
                }
                if (processes.Length == 0)
                {
                    Log(string.Format("错误: 进程未在30秒内启动: {0}", processName), "ERROR");
                    Environment.Exit(1);
                    return;
                }
            }

            process = processes[0];
            Log(string.Format("选中进程: PID={0}, 主窗口: '{1}', 创建时间: {2}", 
                process.Id, process.MainWindowTitle, process.StartTime), "INFO");
        }

        IntPtr hProcess = IntPtr.Zero;
        IntPtr hThread = IntPtr.Zero;
        IntPtr remoteMem = IntPtr.Zero;

        try
        {
            Log("打开进程句柄...", "INFO");
            hProcess = OpenProcess(PROCESS_ALL_ACCESS, false, process.Id);
            if (hProcess == IntPtr.Zero)
            {
                int error = Marshal.GetLastWin32Error();
                Log(string.Format("错误: OpenProcess失败，错误码: {0}", error), "ERROR");
                Log("可能需要管理员权限", "ERROR");
                Environment.Exit(1);
                return;
            }
            Log(string.Format("进程句柄: 0x{0:X}", hProcess.ToInt64()), "INFO");

            bool targetIs32Bit = !Environment.Is64BitOperatingSystem;
            if (Environment.Is64BitOperatingSystem)
            {
                bool targetIsWow64;
                if (!IsWow64Process(hProcess, out targetIsWow64))
                {
                    Log(string.Format("错误: 无法检测目标进程架构，错误码: {0}", Marshal.GetLastWin32Error()), "ERROR");
                    Environment.Exit(1);
                    return;
                }
                targetIs32Bit = targetIsWow64;
            }

            Log(string.Format("进程架构: {0}", targetIs32Bit ? "32-bit" : "64-bit"), "INFO");
            Log(string.Format("注入器架构: {0}", Environment.Is64BitProcess ? "64-bit" : "32-bit"), "INFO");
            if (!targetIs32Bit || Environment.Is64BitProcess)
            {
                Log("错误: 当前版本要求 32 位注入器和 32 位目标游戏", "ERROR");
                Environment.Exit(1);
                return;
            }

            // Check if DLL is already loaded (idempotency)
            Log("检查 DLL 是否已加载...", "INFO");
            string dllName = Path.GetFileName(dllPath);
            IntPtr existingDll = GetRemoteModuleBase(hProcess, dllName);
            if (existingDll != IntPtr.Zero)
            {
                Log(string.Format("DLL 已加载: 0x{0:X}", existingDll.ToInt64()), "SUCCESS");
                Log("already_loaded", "INFO");
                Environment.Exit(0);
                return;
            }
            Log("DLL 未加载，继续注入...", "INFO");

            Log("获取目标进程中的 kernel32.dll 基址...", "INFO");
            IntPtr remoteKernel32 = GetRemoteModuleBase(hProcess, "kernel32.dll");
            if (remoteKernel32 == IntPtr.Zero)
            {
                Log("错误: 未找到 kernel32.dll", "ERROR");
                Environment.Exit(1);
                return;
            }

            Log("获取本地 LoadLibraryW 地址...", "INFO");
            IntPtr localKernel32 = GetModuleHandle("kernel32.dll");
            if (localKernel32 == IntPtr.Zero)
            {
                Log("错误: GetModuleHandle失败", "ERROR");
                Environment.Exit(1);
                return;
            }
            Log(string.Format("本地 kernel32.dll: 0x{0:X}", localKernel32.ToInt64()), "INFO");

            IntPtr localLoadLibrary = GetProcAddress(localKernel32, "LoadLibraryW");
            if (localLoadLibrary == IntPtr.Zero)
            {
                Log("错误: GetProcAddress(LoadLibraryW)失败", "ERROR");
                Environment.Exit(1);
            }
            Log(string.Format("本地 LoadLibraryW: 0x{0:X}", localLoadLibrary.ToInt64()), "INFO");

            long rva = localLoadLibrary.ToInt64() - localKernel32.ToInt64();
            IntPtr remoteLoadLibrary = new IntPtr(remoteKernel32.ToInt64() + rva);
            Log(string.Format("LoadLibraryW RVA: 0x{0:X}", rva), "INFO");
            Log(string.Format("目标进程 LoadLibraryW: 0x{0:X}", remoteLoadLibrary.ToInt64()), "INFO");

            // Use Unicode (UTF-16) encoding for LoadLibraryW to support Chinese paths
            byte[] dllPathBytes = Encoding.Unicode.GetBytes(dllPath + "\0");
            uint dllPathSize = (uint)dllPathBytes.Length;
            Log(string.Format("DLL路径长度: {0} 字节", dllPathSize), "INFO");

            Log("在目标进程分配内存...", "INFO");
            remoteMem = VirtualAllocEx(hProcess, IntPtr.Zero, dllPathSize, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
            if (remoteMem == IntPtr.Zero)
            {
                int error = Marshal.GetLastWin32Error();
                Log(string.Format("错误: VirtualAllocEx失败，错误码: {0}", error), "ERROR");
                Environment.Exit(1);
            }
            Log(string.Format("远程内存地址: 0x{0:X}", remoteMem.ToInt64()), "INFO");

            Log("写入DLL路径到目标进程...", "INFO");
            int bytesWritten = 0;
            bool result = WriteProcessMemory(hProcess, remoteMem, dllPathBytes, dllPathSize, out bytesWritten);
            if (!result)
            {
                int error = Marshal.GetLastWin32Error();
                Log(string.Format("错误: WriteProcessMemory失败，错误码: {0}", error), "ERROR");
                Environment.Exit(1);
            }
            Log(string.Format("写入字节数: {0}", bytesWritten), "INFO");

            Log("创建远程线程执行LoadLibraryW...", "INFO");
            hThread = CreateRemoteThread(hProcess, IntPtr.Zero, 0, remoteLoadLibrary, remoteMem, 0, IntPtr.Zero);
            if (hThread == IntPtr.Zero)
            {
                int error = Marshal.GetLastWin32Error();
                Log(string.Format("错误: CreateRemoteThread失败，错误码: {0}", error), "ERROR");
                Environment.Exit(1);
                return;
            }
            Log(string.Format("远程线程句柄: 0x{0:X}", hThread.ToInt64()), "INFO");

            Log("等待远程线程执行完成...", "INFO");
            uint waitResult = WaitForSingleObject(hThread, 10000);
            if (waitResult != 0)
            {
                Log(string.Format("错误: WaitForSingleObject返回: {0} (超时或失败)", waitResult), "ERROR");
                Log("远程线程执行超时，注入失败", "ERROR");
                Environment.Exit(1);
                return;
            }

            uint exitCode = 0;
            GetExitCodeThread(hThread, out exitCode);
            Log(string.Format("远程线程退出码: 0x{0:X8}", exitCode), "INFO");

            if (exitCode == 0xC0000005)
            {
                Log("错误: ACCESS_VIOLATION (0xC0000005) - DLL加载时崩溃", "ERROR");
                Log("可能原因:", "ERROR");
                Log("  1. DLL与目标进程架构不匹配", "ERROR");
                Log("  2. DllMain初始化代码有bug", "ERROR");
                Log("  3. 缺少运行时依赖", "ERROR");
                Environment.Exit(1);
                return;
            }

            if (exitCode == 0)
            {
                Log("错误: LoadLibraryW返回NULL，DLL加载失败", "ERROR");
                Log("可能原因:", "ERROR");
                Log("  1. DLL文件路径无效", "ERROR");
                Log("  2. DLL依赖缺失", "ERROR");
                Log("  3. DllMain返回FALSE", "ERROR");
                Environment.Exit(1);
                return;
            }

            Log(string.Format("DLL注入成功！基地址: 0x{0:X8}", exitCode), "SUCCESS");

            System.Threading.Thread.Sleep(500);

            Log("==========================================", "INFO");
            Log("注入完成！按 INSERT 键打开菜单", "INFO");
            Log("==========================================", "INFO");
        }
        catch (Exception ex)
        {
            Log(string.Format("异常: {0}: {1}", ex.GetType().Name, ex.Message), "ERROR");
            Log(string.Format("堆栈跟踪: {0}", ex.StackTrace), "ERROR");
            Environment.Exit(1);
        }
        finally
        {
            if (hThread != IntPtr.Zero) CloseHandle(hThread);
            if (hProcess != IntPtr.Zero) CloseHandle(hProcess);
        }
    }
}
