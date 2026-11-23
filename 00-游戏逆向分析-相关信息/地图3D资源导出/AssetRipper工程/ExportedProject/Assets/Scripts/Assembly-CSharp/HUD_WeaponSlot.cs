using UnityEngine;
using UnityEngine.UI;

public class HUD_WeaponSlot : Singleton<HUD_WeaponSlot>
{
	public HUD_WeaponSlotIndividual[] slots;

	private int rapidChangeSlot;

	[SerializeField]
	private RawImage rapidChangeImage;

	private int specialWeaponSlot;

	[SerializeField]
	private RawImage specialWeaponImage;

	[SerializeField]
	private Texture2D[] specialWeaponSprs;

	private static readonly Vector2 SpecialWeaponTipPos;

	private void Update()
	{
	}

	public static void SetImage(int slot, WpnSpriteAsset spriteAsset)
	{
	}

	public static void Clean(int slot)
	{
	}

	public void Select(int slot, bool isRapidChange)
	{
	}

	public void SetSpecialWeaponState(bool isOn)
	{
	}

	public void SetSpecialWeaponSlot(int slot)
	{
	}
}
