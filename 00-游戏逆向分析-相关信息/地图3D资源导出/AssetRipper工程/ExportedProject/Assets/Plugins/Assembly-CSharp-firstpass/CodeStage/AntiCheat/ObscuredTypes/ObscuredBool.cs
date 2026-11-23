using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredBool : IEquatable<ObscuredBool>, IComparable<ObscuredBool>, IComparable<bool>, IComparable
	{
		private static byte cryptoKey;

		[SerializeField]
		private byte currentCryptoKey;

		[SerializeField]
		private int hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private bool fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredBool(bool value)
		{
			currentCryptoKey = 0;
			hiddenValue = 0;
			inited = false;
			fakeValue = false;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(byte newKey)
		{
		}

		public static int Encrypt(bool value)
		{
			return 0;
		}

		public static int Encrypt(bool value, byte key)
		{
			return 0;
		}

		public static bool Decrypt(int value)
		{
			return false;
		}

		public static bool Decrypt(int value, byte key)
		{
			return false;
		}

		public static ObscuredBool FromEncrypted(int encrypted)
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

		public bool GetDecrypted()
		{
			return false;
		}

		private bool InternalDecrypt()
		{
			return false;
		}

		public static implicit operator ObscuredBool(bool value)
		{
			return default;
		}

		public static implicit operator bool(ObscuredBool value)
		{
			return false;
		}

		public override int GetHashCode()
		{
			return 0;
		}

		public override string ToString()
		{
			return null;
		}

		public override bool Equals(object obj)
		{
			return false;
		}

		public bool Equals(ObscuredBool obj)
		{
			return false;
		}

		public int CompareTo(ObscuredBool other)
		{
			return 0;
		}

		public int CompareTo(bool other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
