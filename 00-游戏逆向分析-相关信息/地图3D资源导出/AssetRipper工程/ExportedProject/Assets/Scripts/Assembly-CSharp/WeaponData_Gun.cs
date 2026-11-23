using UnityEngine;

[CreateAssetMenu]
public class WeaponData_Gun : WeaponData
{
	public int clip;

	public int ammo;

	public int clip_Nano;

	public int ammo_Nano;

	public string shotSoundName;

	public float shotsPerMinute;

	public float fireAnimMultiplier;

	public float reloadAnimRatio;

	public string reloadAnimName_C;

	public bool shootBullet;

	public Vector3 bulletFxPos_L;

	public Vector3 bulletFxPos_R;

	public PostureFloat[] perturbMin;

	public PostureFloat[] perturbMax;

	public ChangeMovingRealSize changeMovingRealSize;

	public DelayOneShootData delayOneShootTime;

	public AmmoRecoverAndDecay[] shotReactYaw;

	public AmmoRecoverAndDecay[] shotReactPitch;

	public PostureFloat[] detailPerturbShot;

	public PostureFloat[] detailReactPitchShot;

	public PostureFloat[] detailReactYawShot;

	public PostureFloat[] fullReactYaw;

	public PostureFloat[] fullReactPitch;

	public SideReactDirect sideReactDirect;

	public AmmoRecoverAndDecay[] cameraYawAndPitch;

	public float range;

	public float ammoDamage;

	public float damageVariantionFactor;

	public float damageFactorByDistance;

	public float wallShotDamageRatio;

	public DamageBodyRatio damageBodyRatio;

	public KnifeAttackData[] knifeAttacks;

	public string knifeAnimName;

	public string knifeHitSoundName;

	public DamageBodyRatio knifeDamageBodyRatio;

	public ZoomAction zoomAcion;

	public float zoomInMoveSpeedPenalty;

	public bool giveUpDisable;

	public bool deathDropDisable;

	public float shootIntervalTime => 0f;

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
}
