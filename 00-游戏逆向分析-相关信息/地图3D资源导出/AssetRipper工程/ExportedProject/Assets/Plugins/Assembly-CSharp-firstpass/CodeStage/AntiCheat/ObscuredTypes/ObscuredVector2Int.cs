using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredVector2Int
	{
		[Serializable]
		public struct RawEncryptedVector2Int
		{
			public int x;

			public int y;
		}

		private static int cryptoKey;

		private static readonly Vector2Int zero;

		[SerializeField]
		private int currentCryptoKey;

		[SerializeField]
		private RawEncryptedVector2Int hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private Vector2Int fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		public int x
		{
			get
			{
				return 0;
			}
			set
			{
			}
		}

		public int y
		{
			get
			{
				return 0;
			}
			set
			{
			}
		}

		// C# has no syntax for parameterized property 'Item'.
		public int get_Item(int index)
		{
			return 0;
		}

		public void set_Item(int index, int value)
		{
		}

		private ObscuredVector2Int(Vector2Int value)
		{
			currentCryptoKey = 0;
			hiddenValue = default;
			inited = false;
			fakeValue = default;
			fakeValueActive = false;
		}

		public ObscuredVector2Int(int x, int y)
		{
			currentCryptoKey = 0;
			hiddenValue = default;
			inited = false;
			fakeValue = default;
			fakeValueActive = false;
		}

		public static void SetNewCryptoKey(int newKey)
		{
		}

		public static RawEncryptedVector2Int Encrypt(Vector2Int value)
		{
			return default;
		}

		public static RawEncryptedVector2Int Encrypt(Vector2Int value, int key)
		{
			return default;
		}

		public static RawEncryptedVector2Int Encrypt(int x, int y, int key)
		{
			return default;
		}

		public static Vector2Int Decrypt(RawEncryptedVector2Int value)
		{
			return default;
		}

		public static Vector2Int Decrypt(RawEncryptedVector2Int value, int key)
		{
			return default;
		}

		public static ObscuredVector2Int FromEncrypted(RawEncryptedVector2Int encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public RawEncryptedVector2Int GetEncrypted()
		{
			return default;
		}

		public void SetEncrypted(RawEncryptedVector2Int encrypted)
		{
		}

		public Vector2Int GetDecrypted()
		{
			return default;
		}

		private Vector2Int InternalDecrypt()
		{
			return default;
		}

		private int InternalDecryptField(int encrypted)
		{
			return 0;
		}

		private int InternalEncryptField(int encrypted)
		{
			return 0;
		}

		public static implicit operator ObscuredVector2Int(Vector2Int value)
		{
			return default;
		}

		public static implicit operator Vector2Int(ObscuredVector2Int value)
		{
			return default;
		}

		public static implicit operator Vector2(ObscuredVector2Int value)
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
	}
}
