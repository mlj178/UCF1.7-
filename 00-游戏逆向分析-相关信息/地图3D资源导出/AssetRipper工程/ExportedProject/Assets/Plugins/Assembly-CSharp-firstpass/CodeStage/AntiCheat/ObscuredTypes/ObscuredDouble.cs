using System;
using System.Runtime.InteropServices;
using CodeStage.AntiCheat.Common;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredDouble : IFormattable, IEquatable<ObscuredDouble>, IComparable<ObscuredDouble>, IComparable<double>, IComparable
	{
		[StructLayout((LayoutKind)2)]
		private struct DoubleLongBytesUnion
		{
			[FieldOffset(0)]
			public double d;

			[FieldOffset(0)]
			public long l;

			[FieldOffset(0)]
			public ACTkByte8 b8;
		}

		private static long cryptoKey;

		[SerializeField]
		private long currentCryptoKey;

		[SerializeField]
		private long hiddenValue;

		[SerializeField]
		private ACTkByte8 hiddenValueOldByte8;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private double fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredDouble(double value)
		{
			currentCryptoKey = 0L;
			hiddenValue = 0L;
			hiddenValueOldByte8 = default;
			inited = false;
			fakeValue = 0.0;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(long newKey)
		{
		}

		public static long Encrypt(double value)
		{
			return 0L;
		}

		public static long Encrypt(double value, long key)
		{
			return 0L;
		}

		private static long InternalEncrypt(double value, long key = 0L)
		{
			return 0L;
		}

		public static double Decrypt(long value)
		{
			return 0.0;
		}

		public static double Decrypt(long value, long key)
		{
			return 0.0;
		}

		public static long MigrateEncrypted(long encrypted, byte fromVersion = 0, byte toVersion = 2)
		{
			return 0L;
		}

		public static ObscuredDouble FromEncrypted(long encrypted)
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

		public double GetDecrypted()
		{
			return 0.0;
		}

		private double InternalDecrypt()
		{
			return 0.0;
		}

		public static implicit operator ObscuredDouble(double value)
		{
			return default;
		}

		public static implicit operator double(ObscuredDouble value)
		{
			return 0.0;
		}

		public static explicit operator ObscuredDouble(ObscuredFloat f)
		{
			return default;
		}

		public static ObscuredDouble operator ++(ObscuredDouble input)
		{
			return default;
		}

		public static ObscuredDouble operator --(ObscuredDouble input)
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

		public bool Equals(ObscuredDouble obj)
		{
			return false;
		}

		public int CompareTo(ObscuredDouble other)
		{
			return 0;
		}

		public int CompareTo(double other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
