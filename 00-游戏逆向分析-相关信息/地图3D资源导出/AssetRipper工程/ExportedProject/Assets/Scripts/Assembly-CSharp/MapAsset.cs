using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MapAsset : ScriptableObject
{
	[Serializable]
	public struct Map
	{
		public string sceneName;

		public string mapName;

		public Sprite mapIcon;

		public Texture loadingTex_BL;

		public Texture loadingTex_GR;

		public GameObject gameModePrefabOverride;

		public WeaponLimited weaponLimited;
	}

	public GameMode gameMode;

	public GameObject gameModePrefab;

	public Map[] datas;

	public void UpdateMapDropDown(Dropdown dropdown)
	{
	}

	public virtual void UpdateSettingDropdowns(Dropdown[] dropdowns)
	{
	}

	public virtual void ApplyGameSetting(int mapID, Dropdown[] dropdowns)
	{
	}

	public virtual void OnSettingDropdownValueChange(int dropdownID, int newValue)
	{
	}

	protected void SetListString(List<Dropdown.OptionData> list, string str)
	{
	}

	protected void SetListString(List<Dropdown.OptionData> list, string[] strs)
	{
	}
}
