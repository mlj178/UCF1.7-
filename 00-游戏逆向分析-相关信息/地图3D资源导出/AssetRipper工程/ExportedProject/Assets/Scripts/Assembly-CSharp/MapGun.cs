using UnityEngine;

public class MapGun : MapTrigger
{
	[SerializeField]
	private Sprite otherOccupiedTip;

	[SerializeField]
	private GameObject leg;

	[SerializeField]
	private BoxCollider legCollider;

	[SerializeField]
	private Transform setPos;

	private Player occupier;

	private Weapon weapon;

	[SerializeField]
	private Vector3 defaultEuler;

	[SerializeField]
	private Vector3 wpnPos;

	[SerializeField]
	private Vector3 wpnEuler;

	public QVModel weaponMdl { get; private set; }

	private void Start()
	{
	}

	private void Update()
	{
	}

	public override void Active(Player player)
	{
	}

	public override void OnPlayerExit(Player player)
	{
	}

	public void OnMapWpnRecycle()
	{
	}

	private void ResetEuler()
	{
	}

	public override bool CanInteract()
	{
		return false;
	}

	protected override Sprite GetTipSprite()
	{
		return null;
	}
}
