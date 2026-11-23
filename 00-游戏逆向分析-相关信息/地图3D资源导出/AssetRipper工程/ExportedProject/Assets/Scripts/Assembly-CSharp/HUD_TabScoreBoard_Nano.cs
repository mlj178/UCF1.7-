using RotaryHeart.Lib.SerializableDictionary;
using UnityEngine;

public class HUD_TabScoreBoard_Nano : HUD_TabScoreBoard
{
	public static HUD_TabScoreBoard_Nano instance2;

	[SerializeField]
	private SerializableDictionaryBase<string, Texture> roleIcon;

	protected override void Awake()
	{
	}

	protected override void OnDestroy()
	{
	}

	public static Texture GetRespawnIcon()
	{
		return null;
	}

	public static Texture GetRoleIcon(NanoRole nanoRole)
	{
		return null;
	}
}
