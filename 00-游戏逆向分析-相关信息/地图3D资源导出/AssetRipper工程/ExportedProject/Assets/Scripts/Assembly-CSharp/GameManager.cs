using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using UnityEngine;

public class GameManager : Singleton<GameManager>
{
	public delegate void DamageEvent(ref DamageEventData data);

	public delegate void DeathEvent(DeathEventData data);

	public delegate SpecialKillType SpecialKillChecker(Entity killer, Entity dead);

	public GameObject playerPrefab;

	public GameObject botPrefab;

	public static Player myPlayer;

	public static GameMode gameMode;

	public static WeaponLimited weaponLimited;

	public static bool revengeEnable;

	public static GameObject gameModePrefab;

	[NonSerialized]
	public List<Entity> entityBL_Alive;

	[NonSerialized]
	public List<Entity> entityGR_Alive;

	[NonSerialized]
	public Player[] allPlayers;

	[NonSerialized]
	public List<Player> playersBL;

	[NonSerialized]
	public List<Player> playersBL_Alive;

	[NonSerialized]
	public List<Player> playersGR;

	[NonSerialized]
	public List<Player> playersGR_Alive;

	public WeaponAsset weaponAsset;

	public CharacterAsset characterAsset;

	private NameKeyPool characterPool;

	private NameKeyPool weaponPool;

	public static Dictionary<int, Weapon> WpnDictionary;

	public static Dictionary<int, WeaponData> WpnDataDictionary;

	[CompilerGenerated]
	private static DamageEvent m_DamageEvent_InvalidCheck_Observers;

	[CompilerGenerated]
	private static DamageEvent m_DamageEvent_PreCal_Observers;

	[CompilerGenerated]
	private static DamageEvent m_DamageEvent_PostCal_Observers;

	public static DamageEvent DamageEvent_Post_Observers;

	public static DeathEvent DeathEvent_Observers;

	public static DeathEvent DeathEvent_ForGameRule;

	public static SpecialKillChecker firstAndLastKillChecker;

	[CompilerGenerated]
	private static Action<Player> m_NewPlayerJoinEvent_Observers;

	public static Action<Player> PlayerSpawnEvent_Observers;

	[CompilerGenerated]
	private static Action<Player> m_MyPlayerJoinEvent_Observers;

	public static Action<Player> MyPlayerSpawnEvent_Observers;

	[CompilerGenerated]
	private static DamageEvent m_MyPlayerCasueDamageEvent_Observers;

	[CompilerGenerated]
	private static DamageEvent m_MyPlayerGetDamageEvent_Observers;

	[CompilerGenerated]
	private static DeathEvent m_MyPlayerKillEvent_Observers;

	[CompilerGenerated]
	private static DeathEvent m_MyPlayerDeathEvent_Observers;

	public static Action NewGameRoundStart_Observer;

	[CompilerGenerated]
	private static Action<Weapon> m_GetGrenadeFromBag_Observer;

	private List<RecyclableObject> recyclableObjects;

	public static float dropWpnRecycleTime;

	private int playerCameraChanger;

	public static Team myJoinTeam => Team.BlackList;

	public static bool isNanoMode => false;

	public static int playerCount_BL => 0;

	public static int alivePlayerCount_BL => 0;

	public static int playerCount_GR => 0;

	public static int alivePlayerCount_GR => 0;

	public static Player ace { get; private set; }

	public static bool gameRoundOver { get; private set; }

	public static event DamageEvent DamageEvent_InvalidCheck_Observers
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

	public static event DamageEvent DamageEvent_PreCal_Observers
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

	public static event DamageEvent DamageEvent_PostCal_Observers
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

	public static event Action<Player> NewPlayerJoinEvent_Observers
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

	public static event Action<Player> MyPlayerJoinEvent_Observers
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

	public static event DamageEvent MyPlayerCasueDamageEvent_Observers
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

	public static event DamageEvent MyPlayerGetDamageEvent_Observers
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

	public static event DeathEvent MyPlayerKillEvent_Observers
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

	public static event DeathEvent MyPlayerDeathEvent_Observers
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

	public static event Action<Weapon> GetGrenadeFromBag_Observer
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

	private void Start()
	{
	}

	protected override void OnDestroy()
	{
	}

	public static bool TryGetAce(Player player)
	{
		return false;
	}

	public static void ResetRound(float delay = 0f)
	{
	}

	private IEnumerator RestRoundCoroutine(float delay)
	{
		return null;
	}

	private void AddPlayers()
	{
	}

	private void Test()
	{
	}

	public Player AddPlayer(bool isBot, Team team)
	{
		return null;
	}

	public static int GetSparePlayerIndex()
	{
		return 0;
	}

	public static void LoadWeapon(WeaponAsset asset)
	{
	}

	public static Weapon GiveWeapon(Player player, int weaponIndex, bool autoGiveUp, bool autoSelect)
	{
		return null;
	}

	public static Weapon GiveWeaponByBag(Player player, int weaponIndex)
	{
		return null;
	}

	public static Weapon GetWeapon(int weaponIndex)
	{
		return null;
	}

	public static bool GetWpnData(int weaponIndex, out WeaponData data)
	{
		data = null;
		return false;
	}

	public static string GetWpnName(int weaponIndex)
	{
		return null;
	}

	public static void SetCharacter(Player player, string characterName)
	{
	}

	private static CharacterModel GetCharacter(string characterName)
	{
		return null;
	}

	public static void TakeDamage(DamageEventData data)
	{
	}

	private static void PlayHitFxAndSnd(Entity victim, Vector3 hitPos, DamageType dmgType, string hitSndName, string hitTag, string hitFX)
	{
	}

	private static void DeathEventBroadcast(DeathEventData eventData)
	{
	}

	public static void ReturnLobby()
	{
	}

	public static void GameRoundEnd()
	{
	}

	public static void AddRecyclableObject(RecyclableObject obj)
	{
	}

	public static void RemoveRecyclableObject(RecyclableObject obj)
	{
	}

	public void ClearRecyclableObject()
	{
	}
}
