using UnityEngine;
using UnityEngine.UI;

[CreateAssetMenu]
public class MapAsset_DeathMatch : MapAsset
{
	private static readonly int[] KillDatas;

	private static readonly string[] KillTexts;

	private static readonly string[] WpnSelectTexts;

	public override void UpdateSettingDropdowns(Dropdown[] dropdowns)
	{
	}

	public override void OnSettingDropdownValueChange(int dropdownID, int newValue)
	{
	}

	public override void ApplyGameSetting(int mapID, Dropdown[] dropdowns)
	{
	}
}
