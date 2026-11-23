using RotaryHeart.Lib.SerializableDictionary;
using UnityEngine;

public class HUD_NanoRoleSign : HUD_ProjectionSign
{
	public static SerializableDictionaryBase<string, Sprite> SignDic;

	private Player bindPlayer;

	private bool globalView;

	private bool soldierSign;

	public void Bind(Player player)
	{
	}

	private void OnRoleChange(NanoRole oldRole, NanoRole newRole)
	{
	}

	protected override bool GetVisible()
	{
		return false;
	}
}
