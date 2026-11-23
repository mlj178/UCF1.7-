using System;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredUShort : IFormattable, IEquatable<ObscuredUShort>, IComparable<ObscuredUShort>, IComparable<ushort>, IComparable
	{
		private static ushort cryptoKey;

		private ushort currentCryptoKey;

		private ushort hiddenValue;

		private bool inited;

		private ushort fakeValue;

		private bool fakeValueActive;

		private ObscuredUShort(ushort value)
		{
			currentCryptoKey = 0;
			hiddenValue = 0;
			inited = false;
			fakeValue = 0;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(ushort newKey)
		{
		}

		public static ushort EncryptDecrypt(ushort value)
		{
			return 0;
		}

		public static ushort EncryptDecrypt(ushort value, ushort key)
		{
			return 0;
		}

		public static ObscuredUShort FromEncrypted(ushort encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public ushort GetEncrypted()
		{
			return 0;
		}

		public void SetEncrypted(ushort encrypted)
		{
		}

		public ushort GetDecrypted()
		{
			return 0;
		}

		private ushort InternalDecrypt()
		{
			return 0;
		}

		public static implicit operator ObscuredUShort(ushort value)
		{
			return default;
		}

		public static implicit operator ushort(ObscuredUShort value)
		{
			return 0;
		}

		public static ObscuredUShort operator ++(ObscuredUShort input)
		{
			return default;
		}

		public static ObscuredUShort operator --(ObscuredUShort input)
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

		public bool Equals(ObscuredUShort obj)
		{
			return false;
		}

		public int CompareTo(ObscuredUShort other)
		{
			return 0;
		}

		public int CompareTo(ushort other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
