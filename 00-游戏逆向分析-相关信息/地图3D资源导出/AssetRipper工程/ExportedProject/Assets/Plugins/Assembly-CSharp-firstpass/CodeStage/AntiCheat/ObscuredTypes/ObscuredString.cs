using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public sealed class ObscuredString : IComparable<ObscuredString>, IComparable<string>, IComparable
	{
		private static string cryptoKey;

		[SerializeField]
		private string currentCryptoKey;

		[SerializeField]
		private byte[] hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private string fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		public int Length => 0;

		private ObscuredString()
		{
		}

		private ObscuredString(string value)
		{
		}

		public static void SetNewCryptoKey(string newKey)
		{
		}

		public static string EncryptDecrypt(string value)
		{
			return null;
		}

		public static string EncryptDecrypt(string value, string key)
		{
			return null;
		}

		public static ObscuredString FromEncrypted(string encrypted)
		{
			return null;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public string GetEncrypted()
		{
			return null;
		}

		public void SetEncrypted(string encrypted)
		{
		}

		public string GetDecrypted()
		{
			return null;
		}

		private static byte[] InternalEncrypt(string value)
		{
			return null;
		}

		private static byte[] InternalEncrypt(string value, string key)
		{
			return null;
		}

		private string InternalDecrypt()
		{
			return null;
		}

		public static implicit operator ObscuredString(string value)
		{
			return null;
		}

		public static implicit operator string(ObscuredString value)
		{
			return null;
		}

		public static bool operator ==(ObscuredString a, ObscuredString b)
		{
			return false;
		}

		public static bool operator !=(ObscuredString a, ObscuredString b)
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

		public bool Equals(ObscuredString value)
		{
			return false;
		}

		public bool Equals(ObscuredString value, StringComparison comparisonType)
		{
			return false;
		}

		public int CompareTo(ObscuredString other)
		{
			return 0;
		}

		public int CompareTo(string other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}

		private static byte[] GetBytes(string str)
		{
			return null;
		}

		private static string GetString(byte[] bytes)
		{
			return null;
		}

		private static bool ArraysEquals(byte[] a1, byte[] a2)
		{
			return false;
		}
	}
}
