using System;
using System.Runtime.CompilerServices;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	public static class ObscuredPrefs
	{
		public enum DataType : byte
		{
			Unknown = 0,
			Int = 5,
			UInt = 10,
			String = 15,
			Float = 20,
			Double = 25,
			Decimal = 27,
			Long = 30,
			ULong = 32,
			Bool = 35,
			ByteArray = 40,
			Vector2 = 45,
			Vector3 = 50,
			Quaternion = 55,
			Color = 60,
			Rect = 65
		}

		public enum DeviceLockLevel : byte
		{
			None = 0,
			Soft = 1,
			Strict = 2
		}

		private const byte Version = 2;

		private const string RawNotFound = "{not_found}";

		private const string DataSeparator = "|";

		private static bool alterationReported;

		private static bool foreignSavesReported;

		private static string cryptoKey;

		private static string deviceId;

		private static uint deviceIdHash;

		[Obsolete]
		public static Action onAlterationDetected;

		[CompilerGenerated]
		private static Action m_OnAlterationDetected;

		[Obsolete]
		public static Action onPossibleForeignSavesDetected;

		[CompilerGenerated]
		private static Action m_OnPossibleForeignSavesDetected;

		public static bool preservePlayerPrefs;

		public static DeviceLockLevel lockToDevice;

		public static bool readForeignSaves;

		public static bool emergencyMode;

		private const char DEPRECATED_RAW_SEPARATOR = ':';

		private static string deprecatedDeviceId;

		public static string CryptoKey
		{
			get
			{
				return null;
			}
			set
			{
			}
		}

		public static string DeviceId
		{
			get
			{
				return null;
			}
			set
			{
			}
		}

		[Obsolete]
		internal static string DeviceID
		{
			get
			{
				return null;
			}
			set
			{
			}
		}

		private static uint DeviceIdHash => 0u;

		private static string DeprecatedDeviceId => null;

		public static event Action OnAlterationDetected
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

		public static event Action OnPossibleForeignSavesDetected
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

		public static void ForceLockToDeviceInit()
		{
		}

		[Obsolete]
		internal static void SetNewCryptoKey(string newKey)
		{
		}

		public static void SetInt(string key, int value)
		{
		}

		public static int GetInt(string key)
		{
			return 0;
		}

		public static int GetInt(string key, int defaultValue)
		{
			return 0;
		}

		public static string EncryptIntValue(string key, int value)
		{
			return null;
		}

		public static int DecryptIntValue(string key, string encryptedInput, int defaultValue)
		{
			return 0;
		}

		public static void SetUInt(string key, uint value)
		{
		}

		public static uint GetUInt(string key)
		{
			return 0u;
		}

		public static uint GetUInt(string key, uint defaultValue)
		{
			return 0u;
		}

		public static string EncryptUIntValue(string key, uint value)
		{
			return null;
		}

		public static uint DecryptUIntValue(string key, string encryptedInput, uint defaultValue)
		{
			return 0u;
		}

		public static void SetString(string key, string value)
		{
		}

		public static string GetString(string key)
		{
			return null;
		}

		public static string GetString(string key, string defaultValue)
		{
			return null;
		}

		public static string EncryptStringValue(string key, string value)
		{
			return null;
		}

		public static string DecryptStringValue(string key, string encryptedInput, string defaultValue)
		{
			return null;
		}

		public static void SetFloat(string key, float value)
		{
		}

		public static float GetFloat(string key)
		{
			return 0f;
		}

		public static float GetFloat(string key, float defaultValue)
		{
			return 0f;
		}

		public static string EncryptFloatValue(string key, float value)
		{
			return null;
		}

		public static float DecryptFloatValue(string key, string encryptedInput, float defaultValue)
		{
			return 0f;
		}

		public static void SetDouble(string key, double value)
		{
		}

		public static double GetDouble(string key)
		{
			return 0.0;
		}

		public static double GetDouble(string key, double defaultValue)
		{
			return 0.0;
		}

		private static string EncryptDoubleValue(string key, double value)
		{
			return null;
		}

		private static double DecryptDoubleValue(string key, string encryptedInput, double defaultValue)
		{
			return 0.0;
		}

		public static void SetDecimal(string key, decimal value)
		{
		}

		public static decimal GetDecimal(string key)
		{
			return 0m;
		}

		public static decimal GetDecimal(string key, decimal defaultValue)
		{
			return 0m;
		}

		private static string EncryptDecimalValue(string key, decimal value)
		{
			return null;
		}

		private static decimal DecryptDecimalValue(string key, string encryptedInput, decimal defaultValue)
		{
			return 0m;
		}

		public static void SetLong(string key, long value)
		{
		}

		public static long GetLong(string key)
		{
			return 0L;
		}

		public static long GetLong(string key, long defaultValue)
		{
			return 0L;
		}

		private static string EncryptLongValue(string key, long value)
		{
			return null;
		}

		private static long DecryptLongValue(string key, string encryptedInput, long defaultValue)
		{
			return 0L;
		}

		public static void SetULong(string key, ulong value)
		{
		}

		public static ulong GetULong(string key)
		{
			return 0uL;
		}

		public static ulong GetULong(string key, ulong defaultValue)
		{
			return 0uL;
		}

		private static string EncryptULongValue(string key, ulong value)
		{
			return null;
		}

		private static ulong DecryptULongValue(string key, string encryptedInput, ulong defaultValue)
		{
			return 0uL;
		}

		public static void SetBool(string key, bool value)
		{
		}

		public static bool GetBool(string key)
		{
			return false;
		}

		public static bool GetBool(string key, bool defaultValue)
		{
			return false;
		}

		private static string EncryptBoolValue(string key, bool value)
		{
			return null;
		}

		private static bool DecryptBoolValue(string key, string encryptedInput, bool defaultValue)
		{
			return false;
		}

		public static void SetByteArray(string key, byte[] value)
		{
		}

		public static byte[] GetByteArray(string key)
		{
			return null;
		}

		public static byte[] GetByteArray(string key, byte defaultValue, int defaultLength)
		{
			return null;
		}

		private static string EncryptByteArrayValue(string key, byte[] value)
		{
			return null;
		}

		private static byte[] DecryptByteArrayValue(string key, string encryptedInput, byte defaultValue, int defaultLength)
		{
			return null;
		}

		private static byte[] ConstructByteArray(byte value, int length)
		{
			return null;
		}

		public static void SetVector2(string key, Vector2 value)
		{
		}

		public static Vector2 GetVector2(string key)
		{
			return default;
		}

		public static Vector2 GetVector2(string key, Vector2 defaultValue)
		{
			return default;
		}

		private static string EncryptVector2Value(string key, Vector2 value)
		{
			return null;
		}

		private static Vector2 DecryptVector2Value(string key, string encryptedInput, Vector2 defaultValue)
		{
			return default;
		}

		public static void SetVector3(string key, Vector3 value)
		{
		}

		public static Vector3 GetVector3(string key)
		{
			return default;
		}

		public static Vector3 GetVector3(string key, Vector3 defaultValue)
		{
			return default;
		}

		private static string EncryptVector3Value(string key, Vector3 value)
		{
			return null;
		}

		private static Vector3 DecryptVector3Value(string key, string encryptedInput, Vector3 defaultValue)
		{
			return default;
		}

		public static void SetQuaternion(string key, Quaternion value)
		{
		}

		public static Quaternion GetQuaternion(string key)
		{
			return default;
		}

		public static Quaternion GetQuaternion(string key, Quaternion defaultValue)
		{
			return default;
		}

		private static string EncryptQuaternionValue(string key, Quaternion value)
		{
			return null;
		}

		private static Quaternion DecryptQuaternionValue(string key, string encryptedInput, Quaternion defaultValue)
		{
			return default;
		}

		public static void SetColor(string key, Color32 value)
		{
		}

		public static Color32 GetColor(string key)
		{
			return default;
		}

		public static Color32 GetColor(string key, Color32 defaultValue)
		{
			return default;
		}

		private static string EncryptColorValue(string key, uint value)
		{
			return null;
		}

		public static void SetRect(string key, Rect value)
		{
		}

		public static Rect GetRect(string key)
		{
			return default;
		}

		public static Rect GetRect(string key, Rect defaultValue)
		{
			return default;
		}

		private static string EncryptRectValue(string key, Rect value)
		{
			return null;
		}

		private static Rect DecryptRectValue(string key, string encryptedInput, Rect defaultValue)
		{
			return default;
		}

		public static void SetRawValue(string key, string encryptedValue)
		{
		}

		public static string GetRawValue(string key)
		{
			return null;
		}

		public static DataType GetRawValueType(string value)
		{
			return DataType.Unknown;
		}

		public static string EncryptKey(string key)
		{
			return null;
		}

		public static bool HasKey(string key)
		{
			return false;
		}

		public static void DeleteKey(string key)
		{
		}

		public static void DeleteAll()
		{
		}

		public static void Save()
		{
		}

		private static string GetEncryptedPrefsString(string key, string encryptedKey)
		{
			return null;
		}

		private static string EncryptData(string key, byte[] cleanBytes, DataType type)
		{
			return null;
		}

		internal static byte[] DecryptData(string key, string encryptedInput)
		{
			return null;
		}

		private static uint CalculateChecksum(string input)
		{
			return 0u;
		}

		private static void SavesTampered()
		{
		}

		private static void PossibleForeignSavesDetected()
		{
		}

		private static string GetDeviceId()
		{
			return null;
		}

		private static byte[] EncryptDecryptBytes(byte[] bytes, int dataLength, string key)
		{
			return null;
		}

		private static string DeprecatedDecryptValue(string value)
		{
			return null;
		}

		private static string DeprecatedCalculateChecksum(string input)
		{
			return null;
		}
	}
}
