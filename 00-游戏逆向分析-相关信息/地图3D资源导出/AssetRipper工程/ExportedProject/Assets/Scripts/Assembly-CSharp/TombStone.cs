using System;
using UnityEngine;

public class TombStone : Entity
{
	[NonSerialized]
	public Player owner;

	[SerializeField]
	private GameObject effect;

	private HUD_HealthBar bar;

	[SerializeField]
	private Transform[] hitbox;

	private RecyclableObject RO;

	protected override void Awake()
	{
	}

	protected override void Update()
	{
	}

	private void OnEnable()
	{
	}

	private void OnRecycle()
	{
	}

	private void OnNoRoundRecycle()
	{
	}

	public override void Spawn()
	{
	}

	public override void OnEntityHurt(DamageEventData eventData)
	{
	}

	public override void OnEntityDeath(DeathEventData eventData)
	{
	}

	public void SetOwner(Player owner)
	{
	}

	public override string GetName()
	{
		return null;
	}

	public override Transform GetVisibleHitBox(Ray viewRay)
	{
		return null;
	}
}
