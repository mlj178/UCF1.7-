using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using CodeStage.AntiCheat.ObscuredTypes;
using CustomEvent;
using UnityEngine;

public class Player : Entity
{
	private enum MoveType
	{
		None = 0,
		GroundWalk = 1,
		ClimbStair = 2,
		Swim = 3,
		AirMove = 4
	}

	public enum RespawnType
	{
		Team = 0,
		Stay = 1,
		EnemyTeam = 2
	}

	public static readonly float defaultMoveSpeed;

	public static readonly float playerHeight;

	public static readonly float crouchSubHeight;

	public static readonly float mapCmrHeight;

	public static readonly float mapCmrCrouchSubHeight;

	public static readonly Vector3 playerGravity;

	public PlayerCameraManager cameraManager;

	private Vector2 cameraRotation;

	public Recoil recoil;

	private List<CharacterModel> characters;

	[SerializeField]
	private EffectObj bulletEffect;

	public const float Acceleration = 7.5f;

	public const float Acceleration_Air = 2f;

	public const float JumpPower = 10.5f;

	[CompilerGenerated]
	private Action m_JumpPost_Listener;

	private float jumpDropSndNextPlayTime;

	private float lastFallTime;

	private float heightBeforeFloat;

	private float startMoveTime;

	[NonSerialized]
	public float airVelControlEndTime;

	public PropertyModifier Modifier_MoveSpeedRatio;

	public ClientData clientData;

	public NanoRoleSelect nanoRoleSelect;

	public Nano4T_Data nano4TData;

	public PlayerSkills skills;

	private Coroutine respawn_Coroutine;

	[CompilerGenerated]
	private Action<Player> m_StartRespawn_Listener;

	public RespawnType respawnType;

	[CompilerGenerated]
	private Action<Player> m_NextRespawnInRound_Listener;

	private float nextRegenTime;

	[CompilerGenerated]
	private Action<Player, KeyInputState> m_Interact_Listener;

	public MapTrigger mapTrigger;

	private bool Buff_CameraRotDisabled;

	[CompilerGenerated]
	private RefBool m_CameraRotDisabled_BuffUpdater;

	[CompilerGenerated]
	private RefBool m_JumpDisabled_BuffUpdater;

	[NonSerialized]
	public bool Buff_InfinityAmmo;

	[CompilerGenerated]
	private RefBool m_InfinityAmmo_BuffUpdater;

	public Vector3 mapCameraPos => default;

	public Vector3 mapCameraForward => default;

	public Transform characterContainer { get; private set; }

	public CharacterModel currentCharacter { get; private set; }

	public Vector3 footPos => default;

	public bool autonomousJump { get; private set; }

	public bool isGrounded { get; private set; }

	public string groundMatName { get; private set; }

	public float fallTime => 0f;

	private bool canControlVelInAir => false;

	public Vector3 velocity => default;

	public float MoveSpeedRatio => 0f;

	public PlayerVelocity velData { get; protected set; }

	public PlayerData playerData { get; protected set; }

	public PlayerInput input { get; protected set; }

	public PlayerWeapons wpns { get; private set; }

	public WeaponBag weaponBag { get; protected set; }

	public PlayerMdlInfo modelInfo { get; protected set; }

	public bool isSniper { get; protected set; }

	public Vector3 spawnPos { get; protected set; }

	public bool isRespawning { get; private set; }

	public bool isMyPlayer => false;

	public bool isFocusPlayer => false;

	public bool isFocusPlayerInPV => false;

	public bool isNanoGhost => false;

	public float crouchDuration { get; private set; }

	public bool isCrouching => false;

	public bool walking { get; private set; }

	public ObscuredInt nanoClothCount { get; private set; }

	public float lastStopStartTime { get; private set; }

	public KeyInputState input_Interact { get; private set; }

	public WPN_Gun.AmmoData mapGunAmmo1 { get; private set; }

	public WPN_Gun.AmmoData mapGunAmmo2 { get; private set; }

	public Transform climbStair { get; private set; }

	public bool isClimbing => false;

	public bool Buff_JumpDisabled { get; private set; }

	public string nickName => null;

	public int level => 0;

	public int vipLevel => 0;

	public int kill
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public int death
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public int survival
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public int score
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public HUD_Role.AceSign aceSign
	{
		get
		{
			return HUD_Role.AceSign.None;
		}
		set
		{
		}
	}

	public NanoRole nanoRole
	{
		get
		{
			return NanoRole.Soldier;
		}
		set
		{
		}
	}

	public event Action JumpPost_Listener
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

	public event Action<Player> StartRespawn_Listener
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

	public event Action<Player> NextRespawnInRound_Listener
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

	public event Action<Player, KeyInputState> Interact_Listener
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

	public event RefBool CameraRotDisabled_BuffUpdater
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

	public event RefBool JumpDisabled_BuffUpdater
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

	public event RefBool InfinityAmmo_BuffUpdater
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

	protected override void Awake()
	{
	}

	protected override void Update()
	{
	}

	private void FixedUpdate()
	{
	}

	private void UpdateGroundMatName()
	{
	}

	public void CharacterModelSetting()
	{
	}

	protected override void OnDestroy()
	{
	}

	public bool SetExistentCharacter(string name)
	{
		return false;
	}

	public void SetCharacter(CharacterModel character)
	{
	}

	private void UpdateModelColor()
	{
	}

	private void PhysicalUpdate()
	{
	}

	private void SetGroundState(bool newState)
	{
	}

	public void OnJumpBtnDown()
	{
	}

	public float GetMoveSpeed()
	{
		return 0f;
	}

	public void MoveByLocalDirection(int x, int z)
	{
	}

	public Vector2 GetCameraRotation()
	{
		return default;
	}

	public void AddCameraRotation(float x, float y)
	{
	}

	private void UpdateCameraRotaion()
	{
	}

	public void LookAt(Vector3 dir)
	{
	}

	public void SetWeapon(Weapon weapon)
	{
	}

	private void RecoilShootPostureCheck()
	{
	}

	public override void OnEntityHurt(DamageEventData eventData)
	{
	}

	public override void OnEntityDeath(DeathEventData eventData)
	{
	}

	private void ClearMapObject()
	{
	}

	private void DropWeaponAfterDeath()
	{
	}

	public void SendFireInTheHoleRadio(WeaponClass wpnClass)
	{
	}

	protected override void RemoveFromTeamList(bool onlyAliveList)
	{
	}

	protected override void AddToTeamList(bool isAliveList)
	{
	}

	public void Respawn(float respawnTime, float invisibleTime = 1f)
	{
	}

	public void BreakRespawnCoroutine()
	{
	}

	public override void Spawn()
	{
	}

	private void OnGameRoundEnd()
	{
	}

	public void SetPos(Vector3 pos)
	{
	}

	public bool SelectWeaponBag(int index = -1)
	{
		return false;
	}

	public bool TryPickUpWeapon(Weapon wpn)
	{
		return false;
	}

	public void SetCrouchState(bool crouch)
	{
	}

	public void SetWalkState(bool walk)
	{
	}

	public bool TrySubSkillHPCost(int cost)
	{
		return false;
	}

	public void BreakStopTime()
	{
	}

	private void NanoGhostHPRegen()
	{
	}

	public void SetNanoClothCount(int count)
	{
	}

	public void AddNanoClothCount(int count)
	{
	}

	public void SetInteractInput(KeyInputState state)
	{
	}

	public void FillMapGunAmmo()
	{
	}

	public RecyclableSound Play3dSound(string sndName, int index = -1)
	{
		return null;
	}

	public void PlayBulletEffect(Vector3 position, bool left = false)
	{
	}

	private void OnTriggerEnter(Collider other)
	{
	}

	private void OnTriggerExit(Collider other)
	{
	}

	public void Speak(string msg, HUD_ChatBox.Channel channel = HUD_ChatBox.Channel.All)
	{
	}

	private void UpdateAce()
	{
	}

	private void PlayFootStepSound(bool isRightFoot)
	{
	}

	private void PlayJumpSound(bool isDrop)
	{
	}

	private void ResetDropSndTime()
	{
	}

	private void UpdateFallTime()
	{
	}

	private void UpdateRunState()
	{
	}

	public EffectObj AddPlayerViewEffect(GameObject fxPrefab)
	{
		return null;
	}

	protected override void UpdateBuffProperty()
	{
	}

	public void AddNextRespawnInvincible(float time)
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
