using UnityEngine;
using UnityEngine.UI;

public class HUD_Role : Singleton<HUD_Role>
{
	public enum AceSign
	{
		None = 0,
		Gray = 1,
		Gold = 2
	}

	[SerializeField]
	private Sprite[] aceSprites;

	[SerializeField]
	private AudioClip[] aceAudio;

	private HealthData healthData;

	[SerializeField]
	private RawImage backgroundImage;

	[SerializeField]
	private Image effectImage;

	[SerializeField]
	private RawImage lineImage;

	[SerializeField]
	private Text healthNum;

	[SerializeField]
	private Text armorNum;

	[SerializeField]
	private Material redFlashMat;

	private float lerpAnimEndTime;

	[SerializeField]
	private Image aceImage;

	private static readonly Color green;

	private static readonly Color orange;

	private static readonly Color red;

	private NameKeyPool skillBtnPool;

	private HUD_SkillBtn[] skillBtns;

	protected override void Awake()
	{
	}

	private void Update()
	{
	}

	private void SetColor(Color color, bool flash = false)
	{
	}

	private void OnMyPlayerJoin(Player myPlayer)
	{
	}

	public static void SetAsset(HUD_RoleAsset roleAsset)
	{
	}

	private void UpdateAceSign(AceSign oldSign, AceSign newSign)
	{
	}

	public static HUD_SkillBtn AddSkillBtn(GameObject btnPrefab, Skill bindSkill)
	{
		return null;
	}

	public void RemoveSkillBtn(HUD_SkillBtn btn)
	{
	}

	private void TrySetPos(HUD_SkillBtn btn, int pos)
	{
	}

	public static void StartLerpAnim()
	{
	}
}
