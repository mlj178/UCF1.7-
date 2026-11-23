using UnityEngine;

public class WPN_GrenadeGun : WPN_Gun
{
	[SerializeField]
	private ParticleSystem grenadeFire;

	private AmmoData gunAmmo;

	private AmmoData grenadeAmmo;

	private WD_GrenadeGun realData => null;

	public bool grenadeMode
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	public override void Init()
	{
	}

	private void WPN_GrenadeGun_AnimName_Modifier(ref string value)
	{
	}

	protected override void AmmoSetting()
	{
	}

	public override void FillAmmo()
	{
	}

	public override void AddAmmo(int count)
	{
	}

	protected override void ResetModeChange()
	{
	}

	public override void CrosshairSetting()
	{
	}

	public override void AnimSpeedSetting()
	{
	}

	public override bool GiveUp(bool death = true)
	{
		return false;
	}

	public override void OnSpecialBtnDown()
	{
	}

	public override string GetWpnName()
	{
		return null;
	}

	protected override void GunShootFunction()
	{
	}

	protected override void PlayGunShootSound()
	{
	}

	protected override void PlayCharacterShootAnim()
	{
	}

	public override void PlayGunFire()
	{
	}

	public override WpnSpriteAsset GetWpnSpriteAsset()
	{
		return default;
	}

	public override CharWpnAnimData GetCharWpnAnimData()
	{
		return default;
	}

	protected override bool ShouldPlayBulletEffect()
	{
		return false;
	}
}
