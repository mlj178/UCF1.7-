using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredShort : IFormattable, IEquatable<ObscuredShort>, IComparable<ObscuredShort>, IComparable<short>, IComparable
	{
		private static short cryptoKey;

		[SerializeField]
		private short currentCryptoKey;

		[SerializeField]
		private short hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private short fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredShort(short value)
		{
			currentCryptoKey = 0;
			hiddenValue = 0;
			inited = false;
			fakeValue = 0;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(short newKey)
		{
		}

		public static short EncryptDecrypt(short value)
		{
			return 0;
		}

		public static short EncryptDecrypt(short value, short key)
		{
			return 0;
		}

		public static ObscuredShort FromEncrypted(short encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public short GetEncrypted()
		{
			return 0;
		}

		public void SetEncrypted(short encrypted)
		{
		}

		public short GetDecrypted()
		{
			return 0;
		}

		private short InternalDecrypt()
		{
			return 0;
		}

		public static implicit operator ObscuredShort(short value)
		{
			return default;
		}

		public static implicit operator short(ObscuredShort value)
		{
			return 0;
		}

		public static ObscuredShort operator ++(ObscuredShort input)
		{
			return default;
		}

		public static ObscuredShort operator --(ObscuredShort input)
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

		public bool Equals(ObscuredShort obj)
		{
			return false;
		}

		public int CompareTo(ObscuredShort other)
		{
			return 0;
		}

		public int CompareTo(short other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
