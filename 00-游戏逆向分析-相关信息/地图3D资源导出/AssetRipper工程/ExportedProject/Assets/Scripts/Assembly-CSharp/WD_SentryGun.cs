using UnityEngine;

[CreateAssetMenu]
public class WD_SentryGun : WeaponData
{
	public GameObject sentryGunPrefab;

	public AudioClip SND_Exp;

	public AudioClip SND_Fire;

	public AudioClip SND_PostFire;

	public AudioClip SND_Idle;

	public AudioClip SND_Hit;

	public string GVshotAnimName;

	public GameObject HealthBar;
}
