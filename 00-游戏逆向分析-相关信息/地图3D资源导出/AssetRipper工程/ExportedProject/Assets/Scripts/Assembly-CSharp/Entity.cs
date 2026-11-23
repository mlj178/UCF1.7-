using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using CustomEvent;
using UnityEngine;

public class Entity : MonoBehaviour
{
	[HideInInspector]
	public float baseMoveSpeed;

	[CompilerGenerated]
	private Action<Team> m_team_Listenner;

	protected bool isGhostEntity;

	[NonSerialized]
	public bool isNoHitFeedback;

	private List<Buff> buffs;

	[CompilerGenerated]
	private Action<bool> m_LifeState_Listenner;

	[CompilerGenerated]
	private Ref2Float m_SpeedPenalty_BuffUpdater;

	[CompilerGenerated]
	private Ref2Float m_DamageRate_BuffUpdater;

	[CompilerGenerated]
	private RefBool m_Invincible_BuffUpdater;

	public float speedPenalty { get; private set; }

	public float damageRate { get; private set; }

	public bool isInvincible { get; private set; }

	public HealthData healthData { get; protected set; }

	public bool isDead => false;

	public bool isBlackList => false;

	public bool isGlobalRisk => false;

	public Team team { get; protected set; }

	public Animator characterAnimator { get; protected set; }

	public CharacterController characterController { get; protected set; }

	public event Action<Team> team_Listenner
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

	public event Action<bool> LifeState_Listenner
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

	public event Ref2Float SpeedPenalty_BuffUpdater
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

	public event Ref2Float DamageRate_BuffUpdater
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

	public event RefBool Invincible_BuffUpdater
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

	protected virtual void Awake()
	{
	}

	protected virtual void Update()
	{
	}

	protected virtual void OnDestroy()
	{
	}

	public virtual void SetTeam(Team newTeam)
	{
	}

	protected virtual void RemoveFromTeamList(bool onlyAliveList)
	{
	}

	protected virtual void AddToTeamList(bool isAliveList)
	{
	}

	protected int GetLocalDirection(Vector3 point, bool inverse = false)
	{
		return 0;
	}

	public virtual void Spawn()
	{
	}

	public virtual void OnEntityHurt(DamageEventData eventData)
	{
	}

	public virtual void OnEntityDeath(DeathEventData eventData)
	{
	}

	public Buff AddSpeedPenalty(float penalty, float time, string buffName = "Simple")
	{
		return null;
	}

	public Buff SetDamageRate(float subRate, float time)
	{
		return null;
	}

	public void RemoveBuff(string buffName)
	{
	}

	public void CleanAllBuff(int priority = 0)
	{
	}

	public Buff FindBuff(string buffName)
	{
		return null;
	}

	public void AddBuff(Buff newBuff)
	{
	}

	public Buff TryAddBuff(string buffName, float duration, Func<Buff> buffCreater)
	{
		return null;
	}

	private void UpdateBuff()
	{
	}

	protected virtual void UpdateBuffProperty()
	{
	}

	public void SetGhostEntityState(bool isGhost)
	{
	}

	protected void UpdateColliderLayer()
	{
	}

	public virtual string GetName()
	{
		return null;
	}

	public virtual Transform GetVisibleHitBox(Ray viewRay)
	{
		return null;
	}
}
