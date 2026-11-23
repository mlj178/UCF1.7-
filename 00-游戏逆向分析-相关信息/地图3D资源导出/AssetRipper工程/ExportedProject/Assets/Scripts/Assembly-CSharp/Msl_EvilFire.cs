using UnityEngine;

public class Msl_EvilFire : WPN_GRENADE
{
	[SerializeField]
	private Transform ball;

	[SerializeField]
	private SphereCollider enemyTrigger;

	private float powerProgress;

	public void SetProgress(float progress)
	{
	}

	protected override void PlayExpEffect()
	{
	}
}
