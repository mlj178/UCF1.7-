using System;
using UnityEngine;
using UnityEngine.UI;

public class HUD_Weapon : Singleton<HUD_Weapon>
{
	public enum AmmoBGType
	{
		None = 0,
		Gun = 1,
		RepeatFireOFF = 2,
		RepeatFireOn = 3,
		Energy = 4
	}

	[NonSerialized]
	public Recoil recoil;

	private float clipRedEndTime;

	private RawImage ammo_BG;

	[SerializeField]
	private Text clipText;

	[SerializeField]
	private Text ammoText;

	[SerializeField]
	private RectTransform weaponNameRect;

	[SerializeField]
	private Text weaponNameText;

	[SerializeField]
	private RawImage weaponBGImage;

	[SerializeField]
	private RawImage weaponEffectImage;

	[SerializeField]
	private RawImage weaponLineImage;

	[SerializeField]
	private GameObject infinityAmmo;

	[SerializeField]
	private Texture[] ammoBGTexs;

	[SerializeField]
	private GameObject ammoEnergyBG;

	private Image ammoEnergyGauge;

	private static readonly Vector2 wpnNamePos_L;

	private static readonly Vector2 wpnNamePos_R;

	private static readonly Vector2 AmmoPos_below_1000;

	private static readonly Vector2 AmmoPos_above_1000;

	private static readonly Color Color_BuffClip;

	private static readonly float effectAnimTime;

	private float effectEndTime;

	public WPN_Gun.AmmoData ammoData;

	private float lerpAnimEndTime;

	protected override void Awake()
	{
	}

	private void Update()
	{
	}

	private void AmmoUpdate()
	{
	}

	public static void PlayClipNumFlashFX()
	{
	}

	public static void PlayAmmoLerpAnim()
	{
	}

	public static void SetIcon(WpnSpriteAsset asset)
	{
	}

	public static void SetName(string name)
	{
	}

	public void SetAmmoBGType(AmmoBGType bgType)
	{
	}

	public static void PlayEffect()
	{
	}
}
