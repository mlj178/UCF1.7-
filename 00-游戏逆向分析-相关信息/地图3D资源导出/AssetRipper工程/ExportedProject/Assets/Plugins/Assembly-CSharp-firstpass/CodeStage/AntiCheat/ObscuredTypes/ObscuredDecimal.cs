using System;
using System.Runtime.InteropServices;
using CodeStage.AntiCheat.Common;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredDecimal : IFormattable, IEquatable<ObscuredDecimal>, IComparable<ObscuredDecimal>, IComparable<decimal>, IComparable
	{
		[StructLayout((LayoutKind)2)]
		private struct DecimalLongBytesUnion
		{
			[FieldOffset(0)]
			public decimal d;

			[FieldOffset(0)]
			public long l1;

			[FieldOffset(8)]
			public long l2;

			[FieldOffset(0)]
			public ACTkByte16 b16;
		}

		private static long cryptoKey;

		[SerializeField]
		private long currentCryptoKey;

		[SerializeField]
		private ACTkByte16 hiddenValue;

		[SerializeField]
		private bool inited;

		private decimal fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredDecimal(decimal value)
		{
			currentCryptoKey = 0L;
			hiddenValue = default;
			inited = false;
			fakeValue = 0m;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(long newKey)
		{
		}

		public static decimal Encrypt(decimal value)
		{
			return 0m;
		}

		public static decimal Encrypt(decimal value, long key)
		{
			return 0m;
		}

		private static ACTkByte16 InternalEncrypt(decimal value)
		{
			return default;
		}

		private static ACTkByte16 InternalEncrypt(decimal value, long key)
		{
			return default;
		}

		public static decimal Decrypt(decimal value)
		{
			return 0m;
		}

		public static decimal Decrypt(decimal value, long key)
		{
			return 0m;
		}

		public static ObscuredDecimal FromEncrypted(decimal encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public decimal GetEncrypted()
		{
			return 0m;
		}

		public void SetEncrypted(decimal encrypted)
		{
		}

		public decimal GetDecrypted()
		{
			return 0m;
		}

		private decimal InternalDecrypt()
		{
			return 0m;
		}

		public static implicit operator ObscuredDecimal(decimal value)
		{
			return default;
		}

		public static implicit operator decimal(ObscuredDecimal value)
		{
			return 0m;
		}

		public static explicit operator ObscuredDecimal(ObscuredFloat f)
		{
			return default;
		}

		public static ObscuredDecimal operator ++(ObscuredDecimal input)
		{
			return default;
		}

		public static ObscuredDecimal operator --(ObscuredDecimal input)
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

		public bool Equals(ObscuredDecimal obj)
		{
			return false;
		}

		public int CompareTo(ObscuredDecimal other)
		{
			return 0;
		}

		public int CompareTo(decimal other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
