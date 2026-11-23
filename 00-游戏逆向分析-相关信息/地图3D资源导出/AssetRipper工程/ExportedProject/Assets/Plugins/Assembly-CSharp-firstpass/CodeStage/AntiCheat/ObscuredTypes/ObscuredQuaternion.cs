using System;
using UnityEngine;

namespace CodeStage.AntiCheat.ObscuredTypes
{
	[Serializable]
	public struct ObscuredQuaternion
	{
		[Serializable]
		public struct RawEncryptedQuaternion
		{
			public int x;

			public int y;

			public int z;

			public int w;
		}

		private static int cryptoKey;

		private static readonly Quaternion identity;

		[SerializeField]
		private int currentCryptoKey;

		[SerializeField]
		private RawEncryptedQuaternion hiddenValue;

		[SerializeField]
		private bool inited;

		[SerializeField]
		private Quaternion fakeValue;

		[SerializeField]
		private bool fakeValueActive;

		private ObscuredQuaternion(Quaternion value)
		{
			currentCryptoKey = 0;
			hiddenValue = default;
			inited = false;
			fakeValue = default;
			fakeValueActive = false;
		}

		public ObscuredQuaternion(float x, float y, float z, float w)
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

		public static RawEncryptedQuaternion Encrypt(Quaternion value)
		{
			return default;
		}

		public static RawEncryptedQuaternion Encrypt(Quaternion value, int key)
		{
			return default;
		}

		public static RawEncryptedQuaternion Encrypt(float x, float y, float z, float w, int key)
		{
			return default;
		}

		public static Quaternion Decrypt(RawEncryptedQuaternion value)
		{
			return default;
		}

		public static Quaternion Decrypt(RawEncryptedQuaternion value, int key)
		{
			return default;
		}

		public static ObscuredQuaternion FromEncrypted(RawEncryptedQuaternion encrypted)
		{
			return default;
		}

		public void ApplyNewCryptoKey()
		{
		}

		public void RandomizeCryptoKey()
		{
		}

		public RawEncryptedQuaternion GetEncrypted()
		{
			return default;
		}

		public void SetEncrypted(RawEncryptedQuaternion encrypted)
		{
		}

		public Quaternion GetDecrypted()
		{
			return default;
		}

		private Quaternion InternalDecrypt()
		{
			return default;
		}

		private bool CompareQuaternionsWithTolerance(Quaternion q1, Quaternion q2)
		{
			return false;
		}

		public static implicit operator ObscuredQuaternion(Quaternion value)
		{
			return default;
		}

		public static implicit operator Quaternion(ObscuredQuaternion value)
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
