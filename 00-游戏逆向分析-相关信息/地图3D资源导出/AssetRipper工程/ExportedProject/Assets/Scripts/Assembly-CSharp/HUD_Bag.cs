using UnityEngine;
using UnityEngine.UI;

public class HUD_Bag : Singleton<HUD_Bag>
{
	public HUD_BagButton[] buttons;

	[SerializeField]
	private RawImage[] weaponIcons;

	[SerializeField]
	private GameObject[] vvipBG;

	private Texture[][] iconTextures;

	private bool[][] isVVIP;

	[SerializeField]
	private RectTransform bagIcon;

	[SerializeField]
	private Text bagIndexText;

	private int browseBagID;

	private WeaponBag bag;

	protected override void Awake()
	{
	}

	private void PlayerController_FocusHUD_Listenner(ref string hud)
	{
	}

	private void Update()
	{
	}

	private void MyPlayerJoin(Player player)
	{
	}

	public override void SetVisible(bool visible)
	{
	}

	private void Initialize()
	{
	}

	public void FocusBag(int bagID)
	{
	}

	public void SelectBag(int bagID)
	{
	}
}
