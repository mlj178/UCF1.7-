using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI_GameRoom : Singleton<UI_GameRoom>
{
	[SerializeField]
	private Dropdown matchTypeDropdown;

	[SerializeField]
	private Dropdown mapDropdown;

	[SerializeField]
	private Dropdown winTypeDropdown;

	[SerializeField]
	private Dropdown conditionDropdown;

	[SerializeField]
	private Dropdown weaponSelectDropdown;

	[SerializeField]
	private UI_SelectionGroup wpnBagTab;

	[SerializeField]
	private UI_ItemBox[] wpnSlots;

	[SerializeField]
	private UI_ItemBox_Throw wpnSlot_Throw;

	public static List<ClientData> players;

	private static readonly int[] respawnTime;

	[SerializeField]
	private MapAsset[] mapDatas;

	private MapAsset currentMapAsset;

	private AsyncOperation gameSceneAsync;

	public Dropdown[] gameSettingDropdowns;

	[SerializeField]
	private Dropdown botCountDropDown;

	[SerializeField]
	private Dropdown joinTeamDropDown;

	[SerializeField]
	private List<string> botNames;

	protected override void Awake()
	{
	}

	public void OnMatchTypeChange(int value)
	{
	}

	public void OnWindTypeChange(int value)
	{
	}

	public void OnStartGameBtnDown()
	{
	}

	private void OnInvenLoadFinish()
	{
	}

	private void OnEnterPannel()
	{
	}

	public void OnWpnBagValueChange(int index)
	{
	}

	private void GenerateBotClient()
	{
	}
}
