using UnityEngine;

public class WPN_Missile : RecyclableObject
{
	protected Entity owner;

	protected Team ownerInitalTeam;

	protected WeaponData weaponData;

	protected int sprIndex;

	[SerializeField]
	private string dropSoundName;

	[SerializeField]
	protected Rigidbody rigidBody;

	[SerializeField]
	protected TrailRenderer trailRenderer;

	protected float shootSpeed;

	private Vector3 extraGravity;

	public bool isLegal => false;

	protected virtual void OnCollisionEnter(Collision collision)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	protected override void Work()
	{
	}

	public void SetOwner(Entity newOwner)
	{
	}

	private void FixedUpdate()
	{
	}

	public void SetWeaponData(WeaponData wpnData, int sprIndex)
	{
	}

	protected virtual void SetMissileData(MissileData missileData)
	{
	}
}
