using System;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredByte : IFormattable, IEquatable<ObscuredByte>, IComparable<ObscuredByte>, IComparable<byte>, IComparable
	{
		private static byte cryptoKey;

		private byte currentCryptoKey;

		private byte hiddenValue;

		private bool inited;

		private byte fakeValue;

		private bool fakeValueActive;

		private ObscuredByte(byte value)
		{
			currentCryptoKey = 0;
			hiddenValue = 0;
			inited = false;
			fakeValue = 0;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(byte newKey)
		{
		}

		public static byte EncryptDecrypt(byte value)
		{
			return 0;
		}

		public static void EncryptDecrypt(byte[] value)
		{
		}

		public static byte EncryptDecrypt(byte value, byte key)
		{
			return 0;
		}

		public static void EncryptDecrypt(byte[] value, byte key)
		{
		}

		public static ObscuredByte FromEncrypted(byte encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public byte GetEncrypted()
		{
			return 0;
		}

		public void SetEncrypted(byte encrypted)
		{
		}

		public byte GetDecrypted()
		{
			return 0;
		}

		private byte InternalDecrypt()
		{
			return 0;
		}

		public static implicit operator ObscuredByte(byte value)
		{
			return default;
		}

		public static implicit operator byte(ObscuredByte value)
		{
			return 0;
		}

		public static ObscuredByte operator ++(ObscuredByte input)
		{
			return default;
		}

		public static ObscuredByte operator --(ObscuredByte input)
		{
			return default;
		}

		public override int GetHashCode()
		{
			return 0;
		}

		public override string ToString()
		{
			return null;
		}

		public string ToString(string format)
		{
			return null;
		}

		public string ToString(IFormatProvider provider)
		{
			return null;
		}

		public string ToString(string format, IFormatProvider provider)
		{
			return null;
		}

		public override bool Equals(object obj)
		{
			return false;
		}

		public bool Equals(ObscuredByte obj)
		{
			return false;
		}

		public int CompareTo(ObscuredByte other)
		{
			return 0;
		}

		public int CompareTo(byte other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
