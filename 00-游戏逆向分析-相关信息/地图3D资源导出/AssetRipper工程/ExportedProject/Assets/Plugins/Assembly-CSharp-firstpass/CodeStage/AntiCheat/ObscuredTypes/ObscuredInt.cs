using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredInt : IFormattable, IEquatable<ObscuredInt>, IComparable<ObscuredInt>, IComparable<int>, IComparable
	{
		private static int cryptoKey;

		[SerializeField]
		private int currentCryptoKey;

		[SerializeField]
		private int hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private int fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredInt(int value)
		{
			currentCryptoKey = 0;
			hiddenValue = 0;
			inited = false;
			fakeValue = 0;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(int newKey)
		{
		}

		public static int Encrypt(int value)
		{
			return 0;
		}

		public static int Encrypt(int value, int key)
		{
			return 0;
		}

		public static int Decrypt(int value)
		{
			return 0;
		}

		public static int Decrypt(int value, int key)
		{
			return 0;
		}

		public static ObscuredInt FromEncrypted(int encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public int GetEncrypted()
		{
			return 0;
		}

		public void SetEncrypted(int encrypted)
		{
		}

		public int GetDecrypted()
		{
			return 0;
		}

		private int InternalDecrypt()
		{
			return 0;
		}

		public static implicit operator ObscuredInt(int value)
		{
			return default;
		}

		public static implicit operator int(ObscuredInt value)
		{
			return 0;
		}

		public static implicit operator ObscuredFloat(ObscuredInt value)
		{
			return default;
		}

		public static implicit operator ObscuredDouble(ObscuredInt value)
		{
			return default;
		}

		public static explicit operator ObscuredUInt(ObscuredInt value)
		{
			return default;
		}

		public static ObscuredInt operator ++(ObscuredInt input)
		{
			return default;
		}

		public static ObscuredInt operator --(ObscuredInt input)
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

		public bool Equals(ObscuredInt obj)
		{
			return false;
		}

		public int CompareTo(ObscuredInt other)
		{
			return 0;
		}

		public int CompareTo(int other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
