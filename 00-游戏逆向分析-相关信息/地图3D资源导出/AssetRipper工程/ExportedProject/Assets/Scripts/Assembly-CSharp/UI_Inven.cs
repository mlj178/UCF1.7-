using System.Collections.Generic;
using UnityEngine;

public class UI_Inven : Singleton<UI_Inven>
{
	private static string dataPath;

	[SerializeField]
	private UI_Tab tab;

	[SerializeField]
	private UI_Tab leftTab;

	[SerializeField]
	private UI_SelectionGroup wpnBagTab;

	[SerializeField]
	private UI_ItemBox[] wpnSlots;

	[SerializeField]
	private UI_ItemBox_Throw wpnSlot_Throw;

	[SerializeField]
	private GameObject[] extractWpnBtns;

	[SerializeField]
	private UI_SelectionGroup weaponTabs;

	[SerializeField]
	private UI_ItemPanel itemPanel;

	[SerializeField]
	private Texture2D[] categoryTexs;

	private static Dictionary<int, SO_Item> itemDic;

	private static List<ItemObject> myWeapons;

	private static List<ItemObject> myCharacters;

	private static List<ItemObject> myItems;

	private List<ItemObject> tempItemList;

	private static ItemObject knifeItem;

	private static readonly string defaultBagStr;

	private static List<int> wpnList_Main;

	private static List<int> wpnList_Secondary;

	private static List<int> wpnList_Knife;

	private static List<int> wpnList_Throw;

	private static List<int> characterList;

	public const int ItemID_NewSwat = 1836;

	public const int ItemID_Knife = 108;

	public const int ItemID_PistolAmmo = 231;

	public const int ItemID_ShotGunAmmo = 232;

	public const int ItemID_SmgAmmo = 233;

	public const int ItemID_RifleAmmo = 234;

	public const int ItemID_SniperAmmo = 235;

	public const int ItemID_MgAmmo = 236;

	public const int ItemID_NanoCloth = 468;

	public const int ItemID_NanoAmmo = 469;

	public const int ItemID_Hulk = 522;

	public const int ItemID_Nurse = 554;

	public const int ItemID_Psycho = 3190;

	public const int ItemID_NanoHook = 535;

	private static int[][] wpnBags => null;

	protected override void Awake()
	{
	}

	private void OnEnterPannel()
	{
	}

	private void OnExitPannel()
	{
	}

	public void OnTabValueChange(int value)
	{
	}

	public void OnWpnTabValueChange(int value)
	{
	}

	public void OnCharTabValueChange(int value)
	{
	}

	public void OnItemTabValueChange(int value)
	{
	}

	public static int WeaponItemSort(ItemObject x, ItemObject y)
	{
		return 0;
	}

	private static int ItemNameSort(ItemObject x, ItemObject y)
	{
		return 0;
	}

	public void OnItemBtnDown(UI_ItemBox itemBox)
	{
	}

	private void EquipWeapon(ItemObject newItem)
	{
	}

	private void EquipCharacter(ItemObject item)
	{
	}

	private void EquipItem(UI_ItemBox itemBox)
	{
	}

	public void OnExtractWpnBtnDown(int slot)
	{
	}

	public void OnBagTabValueChange(int bagID)
	{
	}

	public static ItemObject GetWpnBagItem(int bagID, int slot)
	{
		return null;
	}

	private void LoadData()
	{
	}

	public static void SaveData()
	{
	}

	public static int[][] TranslateWpnBag(int[][] bags)
	{
		return null;
	}

	public static SO_Item_Character GetCharacterItem(int itemID)
	{
		return null;
	}

	public static bool TryGetItem(int itemID, out SO_Item result)
	{
		result = null;
		return false;
	}

	private void UpdateItemBox(UI_ItemBox input)
	{
	}

	public void UpdateItemBoxClipBuff(UI_ItemBox input)
	{
	}

	private void ItemSortOut(SO_Item item)
	{
	}

	public static void RandomizeInven(ClientData client)
	{
	}

	public void OnClipBuffUpdate(bool updatePannel = true)
	{
	}

	private void UpdateBagClipBuff()
	{
	}
}
