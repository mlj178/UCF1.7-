using UnityEngine;

public class SentryGun : Entity
{
	private enum State
	{
		Idle = 0,
		Fire = 1,
		PostFire = 2
	}

	[SerializeField]
	private Transform head;

	[SerializeField]
	private ParticleSystem fireFX;

	[SerializeField]
	private GameObject expFX;

	private Vector3 headLocalEuler;

	private RecyclableObject RO;

	private Player owner;

	private RecyclableSound sound;

	private State state;

	private WD_SentryGun wpnData;

	private DamageEventData dmgData;

	private Entity enemy;

	private int nextEnemyID;

	private float nextAttackTime;

	private HUD_HealthBar healthBar;

	protected override void Awake()
	{
	}

	protected override void Update()
	{
	}

	private void OnEnable()
	{
	}

	public void EnterIdleState()
	{
	}

	public override void Spawn()
	{
	}

	private void OnRecycle()
	{
	}

	public override void OnEntityHurt(DamageEventData eventData)
	{
	}

	public override void OnEntityDeath(DeathEventData eventData)
	{
	}

	private void FindEnemy()
	{
	}

	private bool CheckEnemy(Entity target)
	{
		return false;
	}

	private void AttackEnemy()
	{
	}

	private void HeadRotation()
	{
	}

	public void SetData(Player owner, WD_SentryGun wpnData, Vector3 position)
	{
	}

	public override Transform GetVisibleHitBox(Ray viewRay)
	{
		return null;
	}

	private void CreateExplosion()
	{
	}

	private void SetState(State newState)
	{
	}

	public override string GetName()
	{
		return null;
	}

	public void AddHealthBar()
	{
	}
}
