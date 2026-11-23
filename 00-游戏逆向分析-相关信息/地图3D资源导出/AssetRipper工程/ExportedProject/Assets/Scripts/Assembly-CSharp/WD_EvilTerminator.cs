using UnityEngine;

[CreateAssetMenu]
public class WD_EvilTerminator : WD_SkillKnife, IMissileGetter
{
	public MissileData missileData;

	public GameObject gauge;

	public GameObject FX_Power_3rd;

	public GameObject FX_Power_PV;

	public MissileData GetMissileData()
	{
		return default;
	}
}
