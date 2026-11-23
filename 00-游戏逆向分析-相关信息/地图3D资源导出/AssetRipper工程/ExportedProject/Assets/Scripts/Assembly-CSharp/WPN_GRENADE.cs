using System;
using System.Runtime.CompilerServices;
using UnityEngine;

public class WPN_GRENADE : WPN_Missile
{
	[NonSerialized]
	public float expRange;

	[NonSerialized]
	public float expDamage;

	[NonSerialized]
	public float expDmgFactorByDistance;

	[NonSerialized]
	public bool ignoreWall;

	[SerializeField]
	protected GameObject expEffectPrefab;

	[SerializeField]
	protected string expSoundName;

	[SerializeField]
	protected bool expWhenTouchSth;

	protected bool isExped;

	[CompilerGenerated]
	private Action<Entity> m_CauseDamage_Listener;

	public event Action<Entity> CauseDamage_Listener
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	protected override void OnCollisionEnter(Collision collision)
	{
	}

	private void OnTriggerEnter(Collider other)
	{
	}

	protected override void Work()
	{
	}

	protected override void OnLifeTimerEnd()
	{
	}

	protected virtual void TryExplosion()
	{
	}

	protected virtual void PlayExpEffect()
	{
	}

	private void Damage()
	{
	}

	protected virtual DamageEventData GetBasicDamageEventData()
	{
		return default;
	}

	protected override void SetMissileData(MissileData missileData)
	{
	}

	public static void CreateExplosion(Vector3 worldPos, float damage, float range, float distanceDecay, bool ignoreWall, DamageEventData dmgEventData, Action<Entity> damageCallBack = null)
	{
	}
}
