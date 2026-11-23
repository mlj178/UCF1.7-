using System.Runtime.CompilerServices;
using CustomEvent;

public class PlayerController : Singleton<PlayerController>
{
	private string focusHUD;

	public static float activeTime;

	public static float mouseSpeed;

	public static float zoomSpeed;

	[CompilerGenerated]
	private static RefString m_FocusHUD_Listenner;

	private float lastPressWTime;

	public static string FocusHUD => null;

	private Player player => null;

	public static event RefString FocusHUD_Listenner
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

	private void Update()
	{
	}

	private void SkillButton()
	{
	}

	private void CrouchAndWalkButton()
	{
	}

	private void CameraRotation()
	{
	}

	private void MoveButton()
	{
	}

	private void JumpButton()
	{
	}

	private void SelectWeapon()
	{
	}

	private void UseWeapon()
	{
	}
}
