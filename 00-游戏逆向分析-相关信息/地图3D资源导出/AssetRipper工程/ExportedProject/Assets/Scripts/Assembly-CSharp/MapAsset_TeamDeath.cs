using UnityEngine;
using UnityEngine.UI;

[CreateAssetMenu]
public class MapAsset_TeamDeath : MapAsset
{
	public static readonly int[] KillDatas;

	public static readonly string[] KillTexts;

	public static Vector2Int KillConditionTime;

	public static Vector2Int[] TimeDatas;

	public static readonly string[] TimeTexts;

	public static readonly string[] WinType;

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
