using UnityEngine;

[CreateAssetMenu]
public class WD_RPG : WeaponData, IMissileGetter
{
	public MissileData missileData;

	public bool isGrenadeGun;

	public string shotSoundName;

	public float reloadAnimRate;

	public float fireAnimRate;

	public MissileData GetMissileData()
	{
		return default;
	}
}
