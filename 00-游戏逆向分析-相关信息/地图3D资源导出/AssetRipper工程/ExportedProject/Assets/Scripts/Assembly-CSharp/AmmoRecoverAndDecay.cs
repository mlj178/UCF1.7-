using System;

[Serializable]
public struct AmmoRecoverAndDecay
{
	[Serializable]
	public struct Data
	{
		public int ammo;

		public float recover;

		public float decay;
	}

	public Data[] datas;

	public float GetRecover(int ammo)
	{
		return 0f;
	}

	public float GetDecay(int ammo)
	{
		return 0f;
	}
}
