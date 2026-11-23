using System;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredChar : IEquatable<ObscuredChar>, IComparable<ObscuredChar>, IComparable<char>, IComparable
	{
		private static char cryptoKey;

		private char currentCryptoKey;

		private char hiddenValue;

		private bool inited;

		private char fakeValue;

		private bool fakeValueActive;

		private ObscuredChar(char value)
		{
			currentCryptoKey = '\0';
			hiddenValue = '\0';
			inited = false;
			fakeValue = '\0';
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(char newKey)
		{
		}

		public static char EncryptDecrypt(char value)
		{
			return '\0';
		}

		public static char EncryptDecrypt(char value, char key)
		{
			return '\0';
		}

		public static ObscuredChar FromEncrypted(char encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public char GetEncrypted()
		{
			return '\0';
		}

		public void SetEncrypted(char encrypted)
		{
		}

		public char GetDecrypted()
		{
			return '\0';
		}

		private char InternalDecrypt()
		{
			return '\0';
		}

		public static implicit operator ObscuredChar(char value)
		{
			return default;
		}

		public static implicit operator char(ObscuredChar value)
		{
			return '\0';
		}

		public static ObscuredChar operator ++(ObscuredChar input)
		{
			return default;
		}

		public static ObscuredChar operator --(ObscuredChar input)
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

		public string ToString(IFormatProvider provider)
		{
			return null;
		}

		public override bool Equals(object obj)
		{
			return false;
		}

		public bool Equals(ObscuredChar obj)
		{
			return false;
		}

		public int CompareTo(ObscuredChar other)
		{
			return 0;
		}

		public int CompareTo(char other)
		{
			return 0;
		}

		public int CompareTo(object obj)
		{
			return 0;
		}
	}
}
