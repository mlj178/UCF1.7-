using UnityEngine;
using UnityEngine.UI;

public class HUD_Nano4_HumanGauge : SimpleHudBase
{
	[SerializeField]
	private GameObject background;

	[SerializeField]
	private GameObject slotPrefab;

	[SerializeField]
	private Image gauge;

	private RawImage[] slots;

	[SerializeField]
	private Texture[] slotTexs;

	[SerializeField]
	private AnimationHud head;

	[SerializeField]
	private Text atkPowerText;

	[SerializeField]
	private AudioClip heroReadySnd;

	private int deadSoldierCount;

	private int heroNeedCount;

	private bool isNoHero => false;

	public bool isHeroReady => false;

	public bool isSlotType => false;

	protected override void Awake()
	{
	}

	protected override void MyPlayerInit(Player myPlayer)
	{
	}

	private void OnTeamChange(Team team)
	{
	}

	private void OnMyPlayerLifeStateChange(bool isAlive)
	{
	}

	private void Update()
	{
	}

	public void SetTotalSlot(int count)
	{
	}

	public void AddSlot()
	{
	}

	public void ShowHeroReadyTip()
	{
	}

	public override void SetVisible(bool value)
	{
	}

	public void SetSlotVisible(bool visible)
	{
	}

	public void ResetHeroReady()
	{
	}
}
