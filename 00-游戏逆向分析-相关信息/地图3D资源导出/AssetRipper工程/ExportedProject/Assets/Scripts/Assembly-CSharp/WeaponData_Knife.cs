using UnityEngine;

[CreateAssetMenu]
public class WeaponData_Knife : WeaponData
{
	public string knifeAttackAnimName;

	public string knifeHitSoundName;

	public KnifeAttackData[] knifeAttacks;

	public DamageBodyRatio damageBodyRatio;

	public Vector3 attackSpeed;
}
