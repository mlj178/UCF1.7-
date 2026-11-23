using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredVector2
	{
		[Serializable]
		public struct RawEncryptedVector2
		{
			public int x;

			public int y;
		}

		private static int cryptoKey;

		private static readonly Vector2 zero;

		[SerializeField]
		private int currentCryptoKey;

		[SerializeField]
		private RawEncryptedVector2 hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private Vector2 fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		public float x
		{
			get
			{
				return 0f;
			}
			set
			{
			}
		}

		public float y
		{
			get
			{
				return 0f;
			}
			set
			{
			}
		}

		// C# has no syntax for parameterized property 'Item'.
		public float get_Item(int index)
		{
			return 0f;
		}

		public void set_Item(int index, float value)
		{
		}

		private ObscuredVector2(Vector2 value)
		{
			currentCryptoKey = 0;
			hiddenValue = default;
			inited = false;
			fakeValue = default;
			fakeValueActive = false;
		}

		public ObscuredVector2(float x, float y)
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

		public static RawEncryptedVector2 Encrypt(Vector2 value)
		{
			return default;
		}

		public static RawEncryptedVector2 Encrypt(Vector2 value, int key)
		{
			return default;
		}

		public static RawEncryptedVector2 Encrypt(float x, float y, int key)
		{
			return default;
		}

		public static Vector2 Decrypt(RawEncryptedVector2 value)
		{
			return default;
		}

		public static Vector2 Decrypt(RawEncryptedVector2 value, int key)
		{
			return default;
		}

		public static ObscuredVector2 FromEncrypted(RawEncryptedVector2 encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public RawEncryptedVector2 GetEncrypted()
		{
			return default;
		}

		public void SetEncrypted(RawEncryptedVector2 encrypted)
		{
		}

		public Vector2 GetDecrypted()
		{
			return default;
		}

		private Vector2 InternalDecrypt()
		{
			return default;
		}

		private bool CompareVectorsWithTolerance(Vector2 vector1, Vector2 vector2)
		{
			return false;
		}

		private float InternalDecryptField(int encrypted)
		{
			return 0f;
		}

		private int InternalEncryptField(float encrypted)
		{
			return 0;
		}

		public static implicit operator ObscuredVector2(Vector2 value)
		{
			return default;
		}

		public static implicit operator Vector2(ObscuredVector2 value)
		{
			return default;
		}

		public static implicit operator Vector3(ObscuredVector2 value)
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
	}
}
