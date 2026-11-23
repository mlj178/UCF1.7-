using System;
using System.Collections;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;

namespace CodeStage.AntiCheat.Detectors
{
	[DisallowMultipleComponent]
	public class TimeCheatingDetector : ACTkDetectorBase
	{
		public delegate void OnlineTimeCallback(OnlineTimeResult result);

		public delegate void TimeCheatingDetectorEventHandler(CheckResult checkResult, ErrorKind errorKind);

		public struct OnlineTimeResult
		{
			public bool success;

			public string error;

			public long errorResponseCode;

			public double onlineSecondsUtc;

			internal void SetTime(double secondsUtc)
			{
			}

			internal void SetError(string errorText, long responseCode = -1L)
			{
			}

			public override string ToString()
			{
				return null;
			}
		}

		public enum CheckResult
		{
			Unknown = 0,
			CheckPassed = 5,
			WrongTimeDetected = 10,
			CheatDetected = 15,
			Error = 100
		}

		public enum ErrorKind
		{
			NoError = 0,
			IncorrectUri = 3,
			OnlineTimeError = 5,
			NotStarted = 10,
			AlreadyCheckingForCheat = 15,
			Unknown = 100
		}

		public enum RequestMethod
		{
			Head = 0,
			Get = 1
		}

		internal const string ComponentName = "Time Cheating Detector";

		private const string LogPrefix = "[ACTk] Time Cheating Detector: ";

		private const int DefaultTimeoutSeconds = 10;

		private static readonly WaitForEndOfFrame cachedEndOfFrame;

		private static int instancesInScene;

		private static bool gettingOnlineTime;

		[CompilerGenerated]
		private TimeCheatingDetectorEventHandler m_CheatChecked;

		[SerializeField]
		private string requestUrl;

		public RequestMethod requestMethod;

		public int timeoutSeconds;

		public float interval;

		public int realCheatThreshold;

		public int wrongTimeThreshold;

		private readonly string onlineOfflineDifferencePrefsKey;

		private Uri cachedUri;

		private TimeCheatingDetectorEventHandler cheatChecked;

		private float timeElapsed;

		private bool updateAfterPause;

		private double lastOnlineSecondsUtc;

		[CompilerGenerated]
		private Action<ErrorKind> m_Error;

		[CompilerGenerated]
		private Action m_CheckPassed;

		[NonSerialized]
		[Obsolete]
		public int threshold;

		[NonSerialized]
		[Obsolete]
		public string timeServer;

		public string RequestUrl
		{
			get
			{
				return null;
			}
			set
			{
			}
		}

		public ErrorKind LastError { get; private set; }

		public CheckResult LastResult { get; private set; }

		public bool IsCheckingForCheat { get; private set; }

		public static TimeCheatingDetector Instance { get; private set; }

		private static TimeCheatingDetector GetOrCreateInstance => null;

		public event TimeCheatingDetectorEventHandler CheatChecked
		{
			[CompilerGenerated]
			add
			{
			}
			[CompilerGenerated]
			remove
			{
			}
		}

		[Obsolete]
		public event Action<ErrorKind> Error
		{
			[CompilerGenerated]
			add
			{
			}
			[CompilerGenerated]
			remove
			{
			}
		}

		[Obsolete]
		public event Action CheckPassed
		{
			[CompilerGenerated]
			add
			{
			}
			[CompilerGenerated]
			remove
			{
			}
		}

		private void Awake()
		{
		}

		protected override void OnDestroy()
		{
		}

		private void OnLevelWasLoadedNew(Scene scene, LoadSceneMode mode)
		{
		}

		private void OnApplicationPause(bool pauseStatus)
		{
		}

		private void Update()
		{
		}

		public static TimeCheatingDetector AddToSceneOrGetExisting()
		{
			return null;
		}

		public static void StartDetection(TimeCheatingDetectorEventHandler cheatCheckedEventHandler = null)
		{
		}

		public static void StartDetection(float interval, TimeCheatingDetectorEventHandler cheatCheckedEventHandler = null)
		{
		}

		public static void StopDetection()
		{
		}

		public static void Dispose()
		{
		}

		public static IEnumerator GetOnlineTimeCoroutine(string url, OnlineTimeCallback callback, RequestMethod method = RequestMethod.Head)
		{
			return null;
		}

		public static IEnumerator GetOnlineTimeCoroutine(Uri uri, OnlineTimeCallback callback, RequestMethod method = RequestMethod.Head)
		{
			return null;
		}

		public static Task<OnlineTimeResult> GetOnlineTimeTask(string url, RequestMethod method = RequestMethod.Head)
		{
			return null;
		}

		public static Task<OnlineTimeResult> GetOnlineTimeTask(Uri uri, RequestMethod method = RequestMethod.Head)
		{
			return null;
		}

		private static UnityWebRequest GetWebRequest(Uri uri, RequestMethod method)
		{
			return null;
		}

		private static void FillRequestResult(UnityWebRequest request, ref OnlineTimeResult result)
		{
		}

		private static Uri UrlToUri(string url)
		{
			return null;
		}

		private static bool TryGetDate(string source, out DateTime date)
		{
			date = default;
			return false;
		}

		public bool ForceCheck()
		{
			return false;
		}

		public IEnumerator ForceCheckEnumerator()
		{
			return null;
		}

		public Task<CheckResult> ForceCheckTask()
		{
			return null;
		}

		private void StartDetectionInternal(float checkInterval, TimeCheatingDetectorEventHandler cheatCheckedEventHandler = null)
		{
		}

		protected override bool Init(ACTkDetectorBase instance, string detectorName)
		{
			return false;
		}

		protected override void StartDetectionAutomatically()
		{
		}

		protected override bool DetectorHasCallbacks()
		{
			return false;
		}

		protected override void PauseDetector()
		{
		}

		protected override void StopDetectionInternal()
		{
		}

		protected override void DisposeInternal()
		{
		}

		private IEnumerator CheckForCheat()
		{
			return null;
		}

		private void ReportCheckResult()
		{
		}

		private void OnOnlineTimeReceived(OnlineTimeResult result)
		{
		}

		private double GetLocalSecondsUtc()
		{
			return 0.0;
		}

		[Obsolete]
		public static double GetOnlineTime(string server)
		{
			return 0.0;
		}

		[Obsolete]
		public static void SetErrorCallback(Action<ErrorKind> errorCallback)
		{
		}

		[Obsolete]
		public static void StartDetection(Action detectionCallback, int interval)
		{
		}

		[Obsolete]
		public static void StartDetection(Action detectionCallback, Action<ErrorKind> errorCallback, int interval)
		{
		}

		[Obsolete]
		public static void StartDetection(float interval, Action detectionCallback, Action<ErrorKind> errorCallback, Action checkPassedCallback)
		{
		}
	}
}
