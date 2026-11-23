using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredLong : IFormattable, IEquatable<ObscuredLong>, IComparable<ObscuredLong>, IComparable<long>, IComparable
	{
		private static long cryptoKey;

		[SerializeField]
		private long currentCryptoKey;

		[SerializeField]
		private long hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private long fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredLong(long value)
		{
			currentCryptoKey = 0L;
			hiddenValue = 0L;
			inited = false;
			fakeValue = 0L;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(long newKey)
		{
		}

		public static long Encrypt(long value)
		{
			return 0L;
		}

		public static long Decrypt(long value)
		{
			return 0L;
		}

		public static long Encrypt(long value, long key)
		{
			return 0L;
		}

		public static long Decrypt(long value, long key)
		{
			return 0L;
		}

		public static ObscuredLong FromEncrypted(long encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public long GetEncrypted()
		{
			return 0L;
		}

		public void SetEncrypted(long encrypted)
		{
		}

		public long GetDecrypted()
		{
			return 0L;
		}

		private long InternalDecrypt()
		{
			return 0L;
		}

		public static implicit operator ObscuredLong(long value)
		{
			return default;
		}

		public static implicit operator long(ObscuredLong value)
		{
			return 0L;
		}

		public static ObscuredLong operator ++(ObscuredLong input)
		{
			return default;
		}

		public static ObscuredLong operator --(ObscuredLong input)
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

		public bool Equals(ObscuredLong obj)
		{
			return false;
		}

		public int CompareTo(ObscuredLong other)
		{
			return 0;
		}

		public int CompareTo(long other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
