using System;
using UnityEngine;

public class CharacterModel : Model
{
	public enum MoveDirection
	{
		Idle = 0,
		Left = 1,
		Right = 2,
		Forawrd = 3,
		Backward = 4
	}

	[Serializable]
	public enum Sex
	{
		Man = 0,
		Woman = 1
	}

	public Sex sex;

	public bool recycle;

	public Animator characterAnimator;

	public Animator handAnimator;

	[SerializeField]
	private CharacterEffect characterEffect;

	private Renderer[] cvRenderers;

	[SerializeField]
	private AudioClip dieVoice;

	public Transform spine;

	public Transform spine1;

	public Transform neck;

	public string[] socketItemsName;

	private bool isInit;

	public Transform[] hitboxes;

	[NonSerialized]
	public float targetLowerAngle;

	[NonSerialized]
	public float lowerAngle;

	public CharacterVoice voiceAsset;

	public HUD_RoleAsset roleAsset;

	private MoveDirection deathDir;

	private MoveDirection lastMovDir;

	private string lowerAnimName;

	private string lowerAnimName_Temp;

	private string lowerAnimTag;

	private string upperAnimName;

	private CharWpnAnimData animSetting;

	[SerializeField]
	private ParticleSystem aliveEffect;

	[NonSerialized]
	public bool reverseSpineRotation;

	private const int Layer_Upper = 0;

	private const int Layer_Lower = 1;

	private const int Layer_Wpn = 2;

	private const int Layer_Hit = 3;

	private const int Layer_All = 4;

	private const int DieType_Stand = 0;

	private const int DieType_Stand_Headshot = 1;

	private const int DieType_Crouch = 2;

	private const int DieType_Crouch_Headshot = 3;

	private const int DieType_Grenade = 4;

	private const int DieType_LowerHit = 5;

	public Helmet helmet { get; private set; }

	public QVModel bindQvMdl { get; private set; }

	protected override void OnEnable()
	{
	}

	private void Update()
	{
	}

	private void LateUpdate()
	{
	}

	public void BindQvModel(GameObject mdlPrefab)
	{
	}

	public void BindMapGunQvModel(QVModel qvMdl)
	{
	}

	public void RecycleCurQvModel()
	{
	}

	public override void SetOwner(Player newOwner)
	{
	}

	protected override void SetValidOwner()
	{
	}

	protected override void RemoveFromOldOwner()
	{
	}

	public void InitSocketItem()
	{
	}

	public void SetActive(bool active)
	{
	}

	public void PlayHitAnim(Vector3 dmgOrigin)
	{
	}

	public void OnPlayerRespawn()
	{
	}

	public void OnPlayerDeath(bool explosion, bool headshot, bool isHitLower)
	{
	}

	public void PlayJumpAnim(string animName = "M-jump")
	{
	}

	public void PlayGunReloadAnim(string gunName)
	{
	}

	public void PlayWpnAnim(string animName, float duration = 0.2f)
	{
	}

	public void StopWeaponAnim(float duration = 0f)
	{
	}

	public void SetLowerAnimRate(float run, float walk, float crouchWalk)
	{
	}

	public static MoveDirection GetMoveDirByNum(Vector3Int dir)
	{
		return MoveDirection.Idle;
	}

	public static MoveDirection GetMoveDirByNum(int x, int z)
	{
		return MoveDirection.Idle;
	}

	private MoveDirection GetDeathDirection(float angle)
	{
		return MoveDirection.Idle;
	}

	public void SetWeaponAnim(CharWpnAnimData animData)
	{
	}

	private void ResetAnimator()
	{
	}

	private void UpdateLowerAngle()
	{
	}

	private void UpdateAnim()
	{
	}

	private string CombineAnimName(MoveDirection moveDir, bool walk, bool crouch)
	{
		return null;
	}

	private void PlayUpperAnim(string animName, float lerpTime = 0.2f, bool cancelIfPlaying = true)
	{
	}

	private void PlayLowerAnim(string animName, string animTag, float lerpTime = 0.2f, bool cancelIfPlaying = true)
	{
	}

	public void PlayTempLowerAnim(string animName, string animTag, float lerpTime = 0.2f, bool cancelIfPlaying = false)
	{
	}

	public void PlayDeathAnim(string animName, float lerpTime = 0f)
	{
	}

	public void StopDeathAnim()
	{
	}

	private void Nano6CharacterSetting(bool isAlive)
	{
	}

	public Transform GetVisibleHitBox(Ray viewRay)
	{
		return null;
	}

	public static bool CheckHitBox(Ray viewRay, Transform box)
	{
		return false;
	}
}
