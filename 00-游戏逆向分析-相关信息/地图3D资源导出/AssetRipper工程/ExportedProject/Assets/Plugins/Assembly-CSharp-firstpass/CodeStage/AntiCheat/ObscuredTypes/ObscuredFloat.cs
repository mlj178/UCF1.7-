using System;
using System.Runtime.InteropServices;
using CodeStage.AntiCheat.Common;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredFloat : IFormattable, IEquatable<ObscuredFloat>, IComparable<ObscuredFloat>, IComparable<float>, IComparable
	{
		[StructLayout((LayoutKind)2)]
		internal struct FloatIntBytesUnion
		{
			[FieldOffset(0)]
			public float f;

			[FieldOffset(0)]
			public int i;

			[FieldOffset(0)]
			public ACTkByte4 b4;
		}

		private static int cryptoKey;

		[SerializeField]
		private int currentCryptoKey;

		[SerializeField]
		private int hiddenValue;

		[SerializeField]
		private ACTkByte4 hiddenValueOldByte4;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private float fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredFloat(float value)
		{
			currentCryptoKey = 0;
			hiddenValue = 0;
			hiddenValueOldByte4 = default;
			inited = false;
			fakeValue = 0f;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(int newKey)
		{
		}

		public static int Encrypt(float value)
		{
			return 0;
		}

		public static int Encrypt(float value, int key)
		{
			return 0;
		}

		private static int InternalEncrypt(float value, int key = 0)
		{
			return 0;
		}

		public static float Decrypt(int value)
		{
			return 0f;
		}

		public static float Decrypt(int value, int key)
		{
			return 0f;
		}

		public static int MigrateEncrypted(int encrypted, byte fromVersion = 0, byte toVersion = 2)
		{
			return 0;
		}

		public static ObscuredFloat FromEncrypted(int encrypted)
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

		public float GetDecrypted()
		{
			return 0f;
		}

		private float InternalDecrypt()
		{
			return 0f;
		}

		public static implicit operator ObscuredFloat(float value)
		{
			return default;
		}

		public static implicit operator float(ObscuredFloat value)
		{
			return 0f;
		}

		public static ObscuredFloat operator ++(ObscuredFloat input)
		{
			return default;
		}

		public static ObscuredFloat operator --(ObscuredFloat input)
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

		public bool Equals(ObscuredFloat obj)
		{
			return false;
		}

		public int CompareTo(ObscuredFloat other)
		{
			return 0;
		}

		public int CompareTo(float other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
