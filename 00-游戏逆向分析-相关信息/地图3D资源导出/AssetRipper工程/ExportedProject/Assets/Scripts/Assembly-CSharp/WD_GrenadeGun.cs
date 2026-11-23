using UnityEngine;

[CreateAssetMenu]
public class WD_GrenadeGun : WeaponData_Gun, IMissileGetter
{
	public string weaponName2;

	public WpnSpriteAsset spriteAsset2;

	public CharWpnAnimData charWpnAnim2;

	public string shotSoundName2;

	public MissileData missileData;

	public bool haveGMcharAnim => false;

	public override string GetWeaponName(int index)
	{
		return null;
	}

	public override Sprite GetKillMsgIcon(int index)
	{
		return null;
	}

	public override bool GetWeaponSelectImage(int index, out Texture img1, out Texture img2)
	{
		img1 = null;
		img2 = null;
		return false;
	}

	public MissileData GetMissileData()
	{
		return default;
	}
}
