using UnityEngine;

[CreateAssetMenu]
public class WD_Missile : WeaponData, IMissileGetter
{
	public MissileData missileData;

	public MissileData GetMissileData()
	{
		return default;
	}
}
