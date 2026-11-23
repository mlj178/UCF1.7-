using UnityEngine;

public class AssetManager : Singleton<AssetManager>
{
	[SerializeField]
	private GameAsset asset;

	public static float GetAnimSpeed(float input)
	{
		return 0f;
	}

	public static Texture2D GetVipLevelIcon(int level)
	{
		return null;
	}

	public static Texture2D GetSmallLevelIcon(int level)
	{
		return null;
	}
}
