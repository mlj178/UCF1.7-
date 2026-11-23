using UnityEngine;
using UnityEngine.UI;

public class HUD_MapGun : Singleton<HUD_MapGun>
{
	[SerializeField]
	private GameObject exitTip;

	[SerializeField]
	private RawImage backgroundImage;

	[SerializeField]
	private Text ammoText;

	[SerializeField]
	private Text emptyAmmoText;

	private int emptyAmmoTextAnim;

	protected override void Awake()
	{
	}

	private void Start()
	{
	}

	private void OnMyPlayerJoin(Player myPlayer)
	{
	}

	private void OnNanoRoleChange(NanoRole oldRole, NanoRole newRole)
	{
	}

	private void OnLifeStateChange(bool isAlive)
	{
	}

	private void Update()
	{
	}
}
