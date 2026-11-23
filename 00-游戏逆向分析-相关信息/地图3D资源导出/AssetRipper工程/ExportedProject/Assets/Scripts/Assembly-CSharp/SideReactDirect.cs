using System;

[Serializable]
public struct SideReactDirect
{
	[Serializable]
	public struct Data
	{
		public int ammo;

		public float left;

		public float center;

		public float right;
	}

	public float mirrorProbability;

	public Data[] datas;

	public bool GetMirror()
	{
		return false;
	}

	public int GetDirection(int ammo, bool mirror)
	{
		return 0;
	}
}
