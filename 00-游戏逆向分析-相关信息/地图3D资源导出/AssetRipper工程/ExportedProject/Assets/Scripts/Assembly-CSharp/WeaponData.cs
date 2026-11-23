using UnityEngine;
using WeaponNS.Component;

[CreateAssetMenu]
public class WeaponData : ScriptableObject
{
	public int wpnIndex;

	public WeaponClass wpnClass;

	public string weaponName;

	public PlayerViewData viewData;

	public WpnSpriteAsset spriteAsset;

	public bool isVVIP;

	public float changeWeaponAnimRatio;

	public string selectAnimName_C;

	public bool rapidChange;

	public int targetSlot;

	public Weapon.SlotType slotType;

	public CharWpnAnimData charWpnAnim;

	public float moveSpeedPenalty;

	public bool nanoModeLimited;

	public string hitEffectName;

	public GameObject qvMdlPrefab;

	public BotControlData botControlData;

	public ComponentData components;

	public virtual Sprite GetKillMsgIcon(int index)
	{
		return null;
	}

	public virtual string GetWeaponName(int index)
	{
		return null;
	}

	public virtual bool GetWeaponSelectImage(int index, out Texture img1, out Texture img2)
	{
		img1 = null;
		img2 = null;
		return false;
	}
}
