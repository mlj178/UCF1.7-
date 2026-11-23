using UnityEngine;

[CreateAssetMenu]
public class SO_Item_Character : SO_Item
{
	[SerializeField]
	private string characterName;

	[SerializeField]
	private bool nanoModeSpecial;

	public override bool GetSelected()
	{
		return false;
	}

	public string GetCharacterName(Team team)
	{
		return null;
	}
}
