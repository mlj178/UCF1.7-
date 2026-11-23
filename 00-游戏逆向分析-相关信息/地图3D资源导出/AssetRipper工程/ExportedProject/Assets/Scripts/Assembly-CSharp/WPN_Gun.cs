using System;
using CodeStage.AntiCheat.ObscuredTypes;
using UnityEngine;

public class WPN_Gun : Weapon
{
	public enum SemiGunFireLinkState
	{
		None = 0,
		Try = 1,
		Finish = 2
	}

	public class AmmoData
	{
		public ObscuredInt clip;

		public ObscuredInt ammo;

		public ObscuredInt maxClip;

		public ObscuredInt maxAmmo;

		public bool isBuff;

		public bool isMaxClip => false;

		public bool isEmptyClip => false;

		public bool isEmptyAmmo => false;

		public bool canReload => false;

		public bool isAllEmpty => false;

		public void Reload()
		{
		}

		public void Fill()
		{
		}

		public void AddAmmoByMultiplier(int count)
		{
		}

		public void AddClip(int count)
		{
		}

		public void Recover(float rate)
		{
		}

		public void BindHUD()
		{
		}
	}

	private WeaponData_Gun realData;

	[NonSerialized]
	public bool shouldSetFireSpeed;

	public Func<bool> ReloadCheck_Listener;

	protected float lastShootTime;

	protected int recoilDataID;

	public Func<bool> Getter_FireDisabled;

	[NonSerialized]
	public int fireAnim;

	private float nextAllowedShootTime;

	[SerializeField]
	protected ParticleSystem gunFire;

	protected int knifeAttackCount;

	protected int knifeAttackAnim;

	protected int zoomActionCount;

	private int lastZoomIndex;

	public bool isSemiGun { get; protected set; }

	public AmmoData ammoData { get; protected set; }

	public SemiGunFireLinkState semiGunFireLinkState { get; protected set; }

	public bool isSniper => false;

	public int zoomIndex { get; protected set; }

	public bool nextZoomReady { get; protected set; }

	protected override void Update()
	{
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	protected override void OnAnimationExit(string animName, string animTag)
	{
	}

	public override void Init()
	{
	}

	protected override void OnGenerateFromOwner()
	{
	}

	protected virtual void AmmoSetting()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	public override void AnimSpeedSetting()
	{
	}

	protected void UpdateAnimSpeed_Reload()
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	protected virtual void SetBasicRecoilData()
	{
	}

	private void SetRecoilData(int index = 0)
	{
	}

	protected virtual void GunFireChecking()
	{
	}

	public override void OnReloadBtnDown()
	{
	}

	public void TryReload()
	{
	}

	public override void OnSpecialBtnDown()
	{
	}

	public virtual bool CanReload()
	{
		return false;
	}

	protected virtual void Reload()
	{
	}

	protected virtual void ReloadOver()
	{
	}

	private void PreReloadOver()
	{
	}

	public virtual void FillAmmo()
	{
	}

	public virtual void AddAmmo(int count)
	{
	}

	protected void Damage(Ray ray)
	{
	}

	public virtual void PlayGunFire()
	{
	}

	public virtual void StopGunFire()
	{
	}

	private void KnifeAttackEvent(int index)
	{
	}

	protected override KnifeAttackData GetKnifeAttackData(int attackIndex)
	{
		return default;
	}

	protected override string GetKnifeHitSoundName(int attackIndex)
	{
		return null;
	}

	protected override int GetKnifeAttackSprIndex(int attackIndex)
	{
		return 0;
	}

	private void StartKnifeAttack()
	{
	}

	protected virtual void OnKnifeAttackExit()
	{
	}

	protected virtual bool ShouldPlayBulletEffect()
	{
		return false;
	}

	protected void GenerateBullet()
	{
	}

	protected void UseZoom()
	{
	}

	protected void CloseZoom(bool rapidly = false)
	{
	}

	private void OnFireAnimExit()
	{
	}

	public void GunShoot()
	{
	}

	public void GunShoot_NoCheck()
	{
	}

	public void GunShoot_Logic()
	{
	}

	protected virtual void GunShootFunction()
	{
	}

	protected override bool ConsumeAmmo()
	{
		return false;
	}

	private void TryReloadNextFrame()
	{
	}

	protected virtual void PlayGunShootSound()
	{
	}

	protected void BreakAutomaticGunFire()
	{
	}

	private void AutomaticGunStopFire()
	{
	}

	public override void BotControl(Bot bot)
	{
	}

	public void SniperBotControl(Bot bot)
	{
	}

	public override bool CanGetInfinityAmmo()
	{
		return false;
	}

	public override bool GiveUp(bool death = true)
	{
		return false;
	}
}
