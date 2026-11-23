using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using CodeStage.AntiCheat.ObscuredTypes;
using UnityEngine;

public class Weapon : CFAnimator
{
	[Serializable]
	public enum SlotType
	{
		Normal = 0,
		Special = 1,
		Temporary = 2,
		FKey = 3
	}

	public struct KnifeHitData
	{
		public Transform bone;

		public float distance;

		public float angle;
	}

	public WeaponData data;

	protected List<RaycastHit> shootHitTemp;

	protected List<DamageEventData> damageEventTemp;

	protected List<KnifeHitData> knifeHitTemp;

	private static readonly float knifeRangeMultiplier;

	public ObscuredBool moveDisabled;

	public ObscuredBool jumpDisabled;

	public ObscuredBool crouchDisabled;

	public ObscuredBool changeWpnDisabled;

	public ObscuredBool forceWalk;

	public ObscuredBool cameraRotDisabled;

	public Vector3 charOffset;

	[NonSerialized]
	public MapGun bindMapTrigger;

	private bool newWpnTag;

	[CompilerGenerated]
	private Action<int, Entity> m_KnifeAttackHit_Listener;

	[CompilerGenerated]
	private Action<bool> m_Deploy_Listener;

	public Action Setter_AmmoBG;

	public Action<Player> NewValidOwner_Listener;

	public Action<Player> RemoveFromOwner_Listener;

	public bool isUsing => false;

	protected bool isMyWeapon => false;

	protected bool isDead => false;

	public bool fireBtnPressed { get; protected set; }

	public bool isMapGun => false;

	public event Action<int, Entity> KnifeAttackHit_Listener
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

	public event Action<bool> Deploy_Listener
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

	protected override void Update()
	{
	}

	protected virtual void UpdateDisabledSetting(PlayerWeapons wpns)
	{
	}

	public virtual void Init()
	{
	}

	protected virtual void OnGenerateFromOwner()
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	public virtual void Deploy(bool noSelectAnim = false)
	{
	}

	public virtual void UnDeploy(bool temporary = false)
	{
	}

	protected virtual void ResetModeChange()
	{
	}

	public void PlayerViewSetting()
	{
	}

	public void SynchronizeHand()
	{
	}

	public virtual void AnimSpeedSetting()
	{
	}

	public virtual void CrosshairSetting()
	{
	}

	protected void SetMoveSpeedPenalty(float penalty)
	{
	}

	protected virtual void SetCharacterAnim()
	{
	}

	protected override void RemoveFromOldOwner()
	{
	}

	public void OnSelectedFromWeaponPool()
	{
	}

	protected override void SetValidOwner()
	{
	}

	public virtual void OnFireBtnDown()
	{
	}

	public virtual void OnFireBtnPressed()
	{
	}

	public virtual void OnFireBtnUnPressed()
	{
	}

	public virtual void OnSpecialBtnDown()
	{
	}

	public virtual void OnSpecialBtnPressed()
	{
	}

	public virtual void OnSpecialBtnUnPressed()
	{
	}

	public virtual void OnReloadBtnDown()
	{
	}

	public virtual void OnJumpBtnDown()
	{
	}

	protected void SetTrigger(string name)
	{
	}

	protected void ResetTrigger(string name)
	{
	}

	protected void SetBool(string name, bool value)
	{
	}

	protected void SetInteger(string name, int value)
	{
	}

	protected void CrossFadeInFixedTime(string name, float time)
	{
	}

	protected void Play(string animName, float normalizedTime)
	{
	}

	protected virtual KnifeAttackData GetKnifeAttackData(int attackIndex)
	{
		return default;
	}

	protected virtual string GetKnifeHitSoundName(int attackIndex)
	{
		return null;
	}

	protected virtual string GetKnifeHitEffectName(int attackIndex)
	{
		return null;
	}

	protected void CallKnifeAttack(int attackIndex, DamageBodyRatio damageBodyRatio)
	{
	}

	protected virtual int GetKnifeAttackSprIndex(int attackIndex)
	{
		return 0;
	}

	private void TriggerDmgEventAndClear()
	{
	}

	protected bool ShouldDamage(Entity target)
	{
		return false;
	}

	protected void ProjectMissile(GameObject missilePrefab, Vector3 offset, Vector3 euler, Action<WPN_Missile> settingFunc)
	{
	}

	public virtual bool GiveUp(bool death = true)
	{
		return false;
	}

	public virtual void BotControl(Bot bot)
	{
	}

	protected virtual void PlayCharacterShootAnim()
	{
	}

	public virtual string GetWpnName()
	{
		return null;
	}

	public virtual WpnSpriteAsset GetWpnSpriteAsset()
	{
		return default;
	}

	public virtual CharWpnAnimData GetCharWpnAnimData()
	{
		return default;
	}

	public virtual bool CanGetInfinityAmmo()
	{
		return false;
	}

	public void RemoveThisWeapon()
	{
	}

	protected virtual bool ConsumeAmmo()
	{
		return false;
	}
}
