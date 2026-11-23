using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using BotAction;
using BotEvent;
using CodeStage.AntiCheat.ObscuredTypes;
using Pathfinding;
using Pathfinding.Util;
using UnityEngine;

public class Bot : MonoBehaviour
{
	public delegate void ZoomDirectionGetter(ref Vector3 zoomDir, ref int priority);

	private static readonly float Cos10;

	private static readonly float Cos30;

	private static readonly float Cos45;

	public const float EscapeDistance = 10f;

	private BotAbility ability;

	public BotEnemyInfo enemyInfo;

	public bool faceToEnemy;

	private int nextTargetCheckIndex;

	private float nextCheckEnemyInViewTime;

	[NonSerialized]
	public float nextAttackTime;

	[NonSerialized]
	public int knifeAttackType;

	[NonSerialized]
	public float knifeAttackEndTime;

	private float watchOutEndTime;

	private Vector3 watchOutPos;

	public static bool stopAllBot;

	public List<BotActionBase> actionList;

	[CompilerGenerated]
	private ZoomDirectionGetter m_Getter_ZoomDirection;

	private CrabStep crabStepAction;

	private Saunter saunterAction;

	private float nextSelectWpnTime;

	[NonSerialized]
	private List<int> selectWpnActionList;

	[CompilerGenerated]
	private RefInt m_Getter_WeaponSlot;

	private float nextUseSkillCheckTime;

	private AlternativePath alternative;

	private Path path;

	private GraphNode gNode_Nearset;

	private GraphNode gNode_Next;

	private int nextPathVectorID;

	private Vector3 lastStartPoint;

	private Vector3 nextPathPos;

	private Vector3 dirToNextNode;

	private float nextFindPathTime;

	private PathInterpolator interpolator;

	private const float reachDistance = 1.5f;

	private const float reachDistance2D = 1f;

	private const float repathMinTime = 0.25f;

	private const float repathMaxTime = 0.5f;

	[CompilerGenerated]
	private RefPosition m_Destination_Listener;

	private GraphNode nextJumpStartNode;

	private Bot_JumpLink.Link nextJumpLink;

	private float nextJumpTime;

	private float blockedTime;

	private float crouchEndTime;

	private const uint CrouchArea = 1u;

	private const int Rappel = 2;

	private static List<Bot> hangoutList;

	private static int maxHangoutCount;

	private ObscuredBool hangoutTag;

	private bool isDead => false;

	public float abilityLevel
	{
		set
		{
		}
	}

	public Player thisPlayer { get; private set; }

	public Vector3 cameraPos => default;

	public Vector3 cameraFoward => default;

	public Entity tryFindEnemy { get; private set; }

	public bool isStopped => false;

	public Seeker seeker { get; private set; }

	public float pathLength { get; private set; }

	public NanoGuard nanoGuard { get; private set; }

	private bool isArriveJumpStartNode => false;

	private bool canJump => false;

	public event ZoomDirectionGetter Getter_ZoomDirection
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

	public event RefInt Getter_WeaponSlot
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

	public event RefPosition Destination_Listener
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

	public static void InitHangOutCount()
	{
	}

	private void Awake()
	{
	}

	private void Update()
	{
	}

	private void OnDrawGizmosSelected()
	{
	}

	private void UpdateNearestGraphNode()
	{
	}

	private void PathSetting()
	{
	}

	public bool IsPosInReachDistance(Vector3 pos)
	{
		return false;
	}

	public bool IsPosInReachDistance(Vector3 pos, float distance)
	{
		return false;
	}

	private void OnPathComplete(Path newPath)
	{
	}

	private void Move()
	{
	}

	private void JumpCheck()
	{
	}

	private void Jump(float delay = 0f)
	{
	}

	private void TryCrouch()
	{
	}

	private Vector2Int GetMoveStateByDir(Vector3 targetDir)
	{
		return default;
	}

	private void CameraRotation()
	{
	}

	private void OnLifeStateChange(bool isAlive)
	{
	}

	private void TakeDamageEvent(ref DamageEventData eventData)
	{
	}

	private void SpawnDelayEvent()
	{
	}

	private void OnEnterNanoGuardArea(Bot_NanoGuardArea enterArea)
	{
	}

	private void OnExitNanoGuardArea(Bot_NanoGuardArea exitAarea)
	{
	}

	private IEnumerator FindAttackTarget()
	{
		return null;
	}

	private bool TrySetAttackTarget(Entity target)
	{
		return false;
	}

	private bool CheckHitBox(Entity target)
	{
		return false;
	}

	private void CheckAttackTarget()
	{
	}

	private void UseWeapon()
	{
	}

	private void SelectWeapon()
	{
	}

	public void AddSelectWpnAction(int slot)
	{
	}

	private void UseSkill()
	{
	}

	private void OnNanoRoleChange(NanoRole oldRole, NanoRole newRole)
	{
	}

	private void UpdateAction()
	{
	}

	private void OnNanoRoleTableTypeChange(NanoRoleSelect.Type tableType)
	{
	}

	private void OnPlayerSetSkill(Skill newSkill)
	{
	}

	public bool IsPathLengthToEnemyLess(float length)
	{
		return false;
	}

	private void UpdateGhostEntityState()
	{
	}

	public Vector3 GetZoomDirectionByPos(Vector3 pos)
	{
		return default;
	}
}
